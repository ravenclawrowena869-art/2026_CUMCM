"""720-variable continuous LP with a cost-preserving throughput second stage."""
import math
from time import perf_counter
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix, csr_matrix

OPTIONS = {'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9,
           'presolve':True}

def _certificate(result, c, aeq, beq, aub, bub, bounds):
    """Numerical LP KKT evidence in addition to independent physical replay."""
    le=np.array([b[0] for b in bounds],float)
    ue=np.array([b[1] if b[1] is not None else np.inf for b in bounds],float)
    yl=result.lower.marginals;yu=result.upper.marginals;y=result.eqlin.marginals
    residual=c-aeq.T@y-yl-yu
    dual=float(beq@y+le@yl+ue[np.isfinite(ue)]@yu[np.isfinite(ue)])
    comp=[np.max(np.abs((result.x-le)*yl)),np.max(np.abs((ue[np.isfinite(ue)]-result.x[np.isfinite(ue)])*yu[np.isfinite(ue)]))]
    sign=max(float(np.max(-yl)),float(np.max(yu)),0.)
    if aub is not None:
        z=result.ineqlin.marginals
        residual-=aub.T@z;dual+=float(bub@z)
        comp.append(float(np.max(np.abs((bub-aub@result.x)*z))))
        sign=max(sign,float(np.max(z)))
    return {'dual_objective':dual,'primal_dual_gap':float(result.fun-dual),
            'stationarity_max_abs':float(np.max(np.abs(residual))),
            'dual_sign_max_violation':sign,'complementarity_max_abs':float(max(comp))}

def _schedule(rows, vector, eta_c, eta_d):
    # Only negative floating-point noise is clipped; positive actions are retained.
    x=np.array(vector,copy=True)
    noise=(x<0)&(x>=-1e-9)
    x[noise]=0.
    schedule=[]
    for i,row in enumerate(rows):
        g,c,d,u,e=(float(x[k*144+i]) for k in range(5))
        schedule.append({**row,'grid_kwh':g,'charge_kwh':c,'discharge_kwh':d,
                         'curtail_kwh':u,'soc_start_kwh':6000. if i==0 else float(x[576+i-1]),
                         'soc_end_kwh':e,'cost_yuan':row['price_yuan_per_kwh']*g})
    return schedule

def solve(rows, eta_c=0.9, eta_d=0.9):
    if len(rows)!=144 or [r['slot_id'] for r in rows]!=list(range(1,145)):
        raise ValueError('Canonical 144 slots required')
    if not all(math.isfinite(x) and 0<x<=1 for x in [eta_c,eta_d]):
        raise ValueError('Invalid efficiency')
    n=144
    cost=np.zeros(5*n);cost[:n]=[r['price_yuan_per_kwh'] for r in rows]
    if not np.all(np.isfinite(cost)) or min(cost[:n])<=0:
        raise ValueError('Positive finite input prices required')
    aeq=lil_matrix((2*n+1,5*n));beq=np.zeros(2*n+1)
    bounds=[]
    for k in range(5):
        for i,row in enumerate(rows):
            bounds.append([(0.,None),(0.,5000/6),(0.,5000/6),(0.,row['pv_kwh']),(1200.,10800.)][k])
    for i,row in enumerate(rows):
        aeq[i,i]=1;aeq[i,n+i]=-1;aeq[i,2*n+i]=1;aeq[i,3*n+i]=-1
        beq[i]=row['load_kwh']-row['pv_kwh']
        aeq[n+i,n+i]=-eta_c;aeq[n+i,2*n+i]=1/eta_d;aeq[n+i,4*n+i]=1
        if i:
            aeq[n+i,4*n+i-1]=-1
        else:beq[n+i]=6000.
    aeq[-1,-1]=1;beq[-1]=6000.;aeq=aeq.tocsr()
    start=perf_counter()
    one=linprog(cost,A_eq=aeq,b_eq=beq,bounds=bounds,method='highs-ds',options=OPTIONS)
    t1=perf_counter()-start
    if not one.success:
        raise RuntimeError(f'STOP_STAGE1: {one.status} {one.message}')
    cstar=float(one.fun)
    epsilon=max(1e-4,1e-9*abs(cstar))  # Authority R0 BLOCK_SPEC: NEVER widen on failure.
    secondary=np.zeros(5*n);secondary[n:3*n]=1
    aub=csr_matrix(cost.reshape(1,-1));bub=np.array([cstar+epsilon])
    start=perf_counter()
    two=linprog(secondary,A_ub=aub,b_ub=bub,A_eq=aeq,b_eq=beq,bounds=bounds,
                method='highs-ds',options=OPTIONS)
    t2=perf_counter()-start
    if not two.success:
        raise RuntimeError(f'STOP_AND_ESCALATE_EPSILON_C: {two.status} {two.message}')
    schedule=_schedule(rows,two.x,eta_c,eta_d)
    c2=math.fsum(r['cost_yuan'] for r in schedule)
    if c2-cstar>epsilon+1e-8 or c2<cstar-1e-6:
        raise RuntimeError('STOP_STAGE2_COST_PRESERVATION')
    cert1=_certificate(one,cost,aeq,beq,None,None,bounds)
    cert2=_certificate(two,secondary,aeq,beq,aub,bub,bounds)
    summary={'stage1_cost':cstar,'stage2_cost':c2,'stage2_minus_stage1':c2-cstar,
             'epsilon_cost':epsilon,'stage2_throughput_kwh':float(two.fun),
             'method':'highs-ds','options':OPTIONS,
             'numerical_tolerance_provenance':{
                 'epsilon_cost':'R0 BLOCK_SPEC max(1e-4 CNY,1e-9*abs(Cstar)); fixed rule, no retries/widening',
                 'solver_feasibility':'Explicit 1e-9 primal/dual feasibility for margin below R1 1e-6 replay; scipy linprog highs-ds option docstrings',
                 'output':'17 significant decimal digits; clip only negative noise >= -1e-9, then independently replay'},
             'stage1':{'status':int(one.status),'message':one.message,'success':bool(one.success),
                       'runtime_seconds':t1,'iterations':int(one.nit),'objective_cny':cstar,
                       'primal_dual_gap_cny':cert1['primal_dual_gap'],'certificate':cert1},
             'stage2':{'status':int(two.status),'message':two.message,'success':bool(two.success),
                       'runtime_seconds':t2,'iterations':int(two.nit),'objective_throughput_kwh':float(two.fun),
                       'certificate':cert2},'total_solver_runtime_seconds':t1+t2,
             'variable_count':720,'equality_constraint_count':289}
    return {'schedule':schedule,'stage1_schedule':_schedule(rows,one.x,eta_c,eta_d),'solver':summary}
