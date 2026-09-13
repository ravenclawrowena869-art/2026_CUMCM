from __future__ import annotations
from pathlib import Path
from datetime import date,timedelta
import argparse,csv,json,hashlib,time,math,sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from q3.data import load_actuals,load_tariff,load_vintages
from q3.annual_runner import load_frozen_load,stage_pv,date_range
from q3.engine import solve_q3_day
from q3.formal_lp import make_formal_lp_planner
from q3.annual_validator import validate_formal_run
from q3.common import digest,start

BASE=Path('/mnt/data')
INPUTS=BASE/'q3_fyq_r54_run/nested/Q3_FYQ_R5_2_FORMAL14_TASK/Q3_FYQ_R5_2_FORMAL14_TASK/Q3_FYQ_R5_IMPLEMENTATION/inputs'
LOAD=BASE/'q3_fyq_r54_run/nested/Q3_FYQ_R5_2_FORMAL14_TASK/Q3_FYQ_R5_2_FORMAL14_TASK/authority_inputs/Q3_FROZEN_LOAD_FORECAST_R1.csv'
BASELINE=BASE/'Q3_FYQ_R5_4_FORMAL334_DELIVERY'
RELEASE=ROOT/'config/Q3_B1B_CONTROLLER_RELEASE_R5_5.json'
PREREG=ROOT/'config/B1B_PREREGISTRATION_R5_4.json'
OUT=BASE/'Q3_B1B_PRIMARY_R5_5_STREAM'

TRACE_FIELDS=['date','strategy','run_id','slot_id','delivery_start','delivery_end','active_commitment_event_id','q','actual_L','actual_S','actual_available_at','action_decision_time','c_ref','d_ref','c','d','e_before','e_after','r','w','v','price','cost_emergency','source_split_mode','override_c','override_d','fallback_reason','parent_state_hash']
LEDGER_FIELDS=['date','strategy','event_id','run_id','stage','slot_id','previous_active_q','new_active_q','delta_plus','delta_minus','fee_delta','base_q','c_ref','d_ref','price_value','forecast_vintage_id','load_forecast_id','issue_time','known_at_max','parent_commitment_hash']
DAILY_FIELDS=['date','B1B_total_cost','B1B_emergency_kwh','B1B_initial_soc','B1B_terminal_soc','hard_violation_count','base_planned_cost_yuan','adjustment_cost_yuan','emergency_cost_yuan','solver_runtime_seconds','numerical_recovery_count']
CONT_FIELDS=['date','strategy','initial_soc_kwh','previous_terminal_soc_kwh','terminal_soc_kwh','initial_state_hash','final_state_hash','continuity_residual_kwh']
LAMBDA_FIELDS=['date','stage','lambda','e_new','e_ref','valid_history_count','training_start_date','training_end_date','training_cutoff_date','window_id','method_id','loss_id','fallback_status','history_source_hash','pv_new_source_hash','pv_ref_reconstruction_hash','new_forecast_id']

def jload(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for c in iter(lambda:f.read(1<<20),b''):h.update(c)
 return h.hexdigest()
def write_json(p,x): Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n',encoding='utf-8')
def append_csv(path,rows,fields):
 path=Path(path); new=not path.exists()
 with path.open('a',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore')
  if new:w.writeheader()
  for r in rows:w.writerow({k:r.get(k,'') for k in fields})
def blend(ref,new,lam,first_slot):
 vals=list(ref['values'])
 for i in range(first_slot-1,144): vals[i]=lam*float(new['values'][i])+(1-lam)*float(ref['values'][i])
 return {'forecast_id':f"B1B:{new['forecast_id']}:{digest([lam,ref['forecast_id'],first_slot])[:16]}", 'known_at':new['known_at'],'values':vals,'interpolation':'PV_HOURLY_LINEAR_CAUSAL_BOUNDARY_V1','boundary_mode':'B1B_BLEND_AFTER_A4'}
def loss(vals,actual,slots,kind='MAE'):
 es=[float(vals[t-1])-float(actual[t-1]['pv_kwh']) for t in slots]
 if kind=='RMSE':return math.sqrt(sum(e*e for e in es)/len(es))
 return sum(abs(e) for e in es)/len(es)

class L1History:
 def __init__(self,window=28,min_history=14,loss_id='MAE'):
  self.window=window;self.min_history=min_history;self.loss_id=loss_id;self.hist={6:[],12:[],18:[]}
 def lambdas(self,day):
  res={}
  for s in (6,12,18):
   selected=self.hist[s][-self.window:]
   n=len(selected)
   if n<self.min_history:
    lam=1.;en=er=None;fb='FALLBACK_TO_B1A_INSUFFICIENT_HISTORY'
   else:
    en=sum(x['L_new'] for x in selected)/n; er=sum(x['L_ref'] for x in selected)/n
    if en+er<=1e-12:lam=1.;fb='FALLBACK_TO_B1A_DEGENERATE_ZERO_LOSS'
    else:lam=min(max(er/(en+er),0.),1.);fb='NONE'
   res[s]=(lam,en,er,selected,fb)
  return res
 def record(self,day,legal,refs,actual):
  for s,first in ((6,37),(12,73),(18,109)):
   slots=range(first,145)
   self.hist[s].append({'date':day,'L_new':loss(legal[s]['values'],actual,slots,self.loss_id),'L_ref':loss(refs[s]['values'],actual,slots,self.loss_id)})

def legal_day(vintage_by_issue,day):
 pv={}; prefix=[]
 for st in (0,6,12,18):
  x=stage_pv(vintage_by_issue,day,st,prefix);pv[st]=x;prefix=x['values'][:(st+6)*6]
 return pv

def build_schedule(actuals,vintage_by_issue,end_day='2025-12-31'):
 hist=L1History(28,14,'MAE'); schedules={}; ledger=[]
 d=date(2025,1,2); end=date.fromisoformat(end_day)
 while d<=end:
  day=d.isoformat(); actual=actuals[day]; legal=legal_day(vintage_by_issue,day); lams=hist.lambdas(day)
  eff={0:legal[0]}; refs={}
  for s,first in ((6,37),(12,73),(18,109)):
   refs[s]=eff[0] if s==6 else eff[6] if s==12 else eff[12]
   lam,en,er,sel,fb=lams[s]
   eff[s]=blend(refs[s],legal[s],lam,first)
   ledger.append({'date':day,'stage':s,'lambda':lam,'e_new':en,'e_ref':er,'valid_history_count':len(sel),'training_start_date':sel[0]['date'] if sel else None,'training_end_date':sel[-1]['date'] if sel else None,'training_cutoff_date':(d-timedelta(days=1)).isoformat(),'window_id':'TRAILING_28_VALID_DAYS','method_id':'L1_INVERSE_OOS_ERROR','loss_id':'MAE','fallback_status':fb,'history_source_hash':digest(sel),'pv_new_source_hash':digest(legal[s]),'pv_ref_reconstruction_hash':digest(refs[s]),'new_forecast_id':legal[s]['forecast_id']})
  schedules[day]=eff
  hist.record(day,legal,refs,actual)
  d+=timedelta(days=1)
 return schedules,ledger

def load_ctx():
 release=jload(RELEASE); prereg=jload(PREREG); cfgsnap=jload(BASELINE/'config_snapshot.json')
 actuals=load_actuals(INPUTS/'attachment2.xlsx'); prices=[r['price_yuan_per_kwh'] for r in load_tariff(INPUTS/'attachment1.xlsx')]
 vint=load_vintages(INPUTS/'attachment3.xlsx'); vmap={x['issue_time']:x for x in vint}; loads=load_frozen_load(LOAD)
 rb=release['runtime_bindings']; checks={'pv_vintages_attachment3_sha256':sha(INPUTS/'attachment3.xlsx'),'actual_attachment2_sha256':sha(INPUTS/'attachment2.xlsx'),'tariff_attachment1_sha256':sha(INPUTS/'attachment1.xlsx'),'frozen_load_sha256':sha(LOAD),'formal_lp_sha256':sha(BASELINE/'code/formal_lp.py'),'engine_baseline_sha256':sha(BASELINE/'code/engine.py'),'ledger_sha256':sha(BASELINE/'code/ledger.py'),'validator_sha256':sha(BASELINE/'code/validator.py'),'annual_validator_sha256':sha(BASELINE/'code/annual_validator.py'),'formal334_baseline_delivery_sha256':sha(BASE/'Q3_FYQ_R5_4_FORMAL334_DELIVERY.zip')}
 if any(checks[k]!=v for k,v in rb.items()):raise RuntimeError('B1B_RUNTIME_BINDING_MISMATCH')
 cfg=dict(cfgsnap['formal_b1a']); cfg['strategy_id']='B1B';cfg['pv_vintage_policy']='BLENDED_TRUST_WITH_FROZEN_CAUSAL_LAMBDA';cfg['formal_release']={'status':'RELEASED','authority':release['authority'],'source_hash':sha(RELEASE),'release_id':release['release_id'],'scope':'FORMAL_334D_B1B_PRIMARY'}
 return release,prereg,cfg,actuals,prices,vmap,loads,checks

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--chunk-days',type=int,default=50); args=ap.parse_args()
 OUT.mkdir(exist_ok=True)
 release,prereg,cfg,actuals,prices,vmap,loads,checks=load_ctx()
 schedules,lambda_ledger=build_schedule(actuals,vmap)
 if not (OUT/'lambda_ledger_all.csv').exists():append_csv(OUT/'lambda_ledger_all.csv',lambda_ledger,LAMBDA_FIELDS)
 dates=date_range('2025-02-01','2025-12-31')
 cp=jload(OUT/'checkpoint.json') if (OUT/'checkpoint.json').exists() else None
 if cp and cp.get('status')=='COMPLETE': print('ALREADY_COMPLETE'); return 0
 idx=int(cp['days_completed']) if cp else 0
 stop=min(idx+args.chunk_days,len(dates))
 if cp:
  soc=float(cp['soc_kwh']); state_hash=cp['state_hash']; prev_term=float(cp['last_terminal_soc_kwh'])
 else:
  soc=6000.;state_hash=digest({'protocol':'Q3_B1B_FORMAL334_CONSECUTIVE_STATE_R5_5','strategy':'B1B','date':dates[0],'initial_soc_kWh':6000.,'release_id':release['release_id']});prev_term=6000.
 started=time.perf_counter();recoveries=0
 for j in range(idx,stop):
  day=dates[j]; initial=soc; init_hash=state_hash
  run=solve_q3_day(date=day,load_forecast_provider=loads[day],pv_vintage_provider=schedules[day],update_stages=[0,6,12,18],initial_soc=initial,actual_rows=actuals[day],prices=prices,config=cfg,initial_state_hash=init_hash,planner=make_formal_lp_planner(cfg))
  val=validate_formal_run(run)
  if val['status']!='PASS':raise RuntimeError(f'B1B_DAY_VALIDATION_FAIL:{day}')
  m=val['metrics']; cont=abs(initial-prev_term) if j else abs(initial-6000.)
  append_csv(OUT/'per_slot_trace.csv',[{'date':day,'strategy':'B1B',**r} for r in run['trace']],TRACE_FIELDS)
  led=[]
  for ev in run['events']:
   for r in ev['rows']:led.append({'date':day,'strategy':'B1B','event_id':ev['event_id'],**r})
  append_csv(OUT/'stage_ledger.csv',led,LEDGER_FIELDS)
  dayrec=sum(int((c.get('solver_metadata') or {}).get('numerical_recovery_count',0)) for c in run['stage_calls']);recoveries+=dayrec
  solver_rt=sum(float(c.get('runtime_seconds',0)) for c in run['stage_calls'])
  append_csv(OUT/'paired_daily_summary.csv',[{'date':day,'B1B_total_cost':m['total_cost_yuan'],'B1B_emergency_kwh':m['emergency_energy_kwh'],'B1B_initial_soc':initial,'B1B_terminal_soc':m['terminal_soc_kwh'],'hard_violation_count':val['failure_count'],'base_planned_cost_yuan':m['base_planned_cost_yuan'],'adjustment_cost_yuan':m['adjustment_cost_yuan'],'emergency_cost_yuan':m['emergency_cost_yuan'],'solver_runtime_seconds':solver_rt,'numerical_recovery_count':dayrec}],DAILY_FIELDS)
  append_csv(OUT/'soc_continuity_report.csv',[{'date':day,'strategy':'B1B','initial_soc_kwh':initial,'previous_terminal_soc_kwh':prev_term,'terminal_soc_kwh':m['terminal_soc_kwh'],'initial_state_hash':init_hash,'final_state_hash':run['final_state_hash'],'continuity_residual_kwh':cont}],CONT_FIELDS)
  with (OUT/'solver_metadata.jsonl').open('a',encoding='utf-8') as f:
   for c in run['stage_calls']:f.write(json.dumps({'date':day,'strategy':'B1B','stage':c['stage'],'solver_status':c['solver_status'],'runtime_seconds':c['runtime_seconds'],'solver_metadata':c['solver_metadata']},ensure_ascii=False)+'\n')
  with (OUT/'validator_report.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps({'date':day,'strategy':'B1B','status':val['status'],'failure_count':val['failure_count'],'metrics':m},ensure_ascii=False)+'\n')
  with (OUT/'input_provenance.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps({'date':day,'strategy':'B1B','run_id':run['run_id'],'initial_state_hash':run['initial_state_hash'],'final_state_hash':run['final_state_hash'],'load_hash':digest(run['source_inputs']['load_forecast']),'pv_hash':digest(run['source_inputs']['pv_forecasts']),'actual_hash':digest(run['source_inputs']['actual_rows']),'prices_hash':digest(run['source_inputs']['prices']),'release_sha256':sha(RELEASE),'preregistration_sha256':sha(PREREG)},ensure_ascii=False)+'\n')
  soc=float(m['terminal_soc_kwh']);prev_term=soc;state_hash=run['final_state_hash']
  write_json(OUT/'checkpoint.json',{'schema':'Q3_B1B_CHECKPOINT_R5_5_V1','status':'COMPLETE' if j+1==len(dates) else 'IN_PROGRESS','days_completed':j+1,'last_date':day,'soc_kwh':soc,'last_terminal_soc_kwh':soc,'state_hash':state_hash,'release_sha256':sha(RELEASE),'preregistration_sha256':sha(PREREG)})
  if (j+1)%10==0 or j==idx or j+1==stop:print(f'B1B_PROGRESS {j+1}/{len(dates)} {day} SOC={soc:.3f} COST={m["total_cost_yuan"]:.2f} LAMBDA6={next(x["lambda"] for x in lambda_ledger if x["date"]==day and x["stage"]==6):.3f}',flush=True)
 print(json.dumps({'status':'CHUNK_COMPLETE','from_day':idx+1,'to_day':stop,'recoveries':recoveries,'elapsed':time.perf_counter()-started}))
 return 0
if __name__=='__main__':raise SystemExit(main())
