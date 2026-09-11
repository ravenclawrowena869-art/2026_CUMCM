Q2_MATH_CONTRACT_ID = CUMCM2026_C_Q2_MATH_CONTRACT_R1

# Q2 正式优化数学合同 R1

ACTIVE_ROLE=XXT_MATHEMATICAL。日期：2026-09-11。
退出：`HOLD_FOR_EVIDENCE`。合同标识已签发；正式 implementation release 尚未签发。标识与有效内容由相邻 manifest 的 SHA256 绑定，不得把“已有 ID”等同于“物理假设全部获批”。

本轮交付数学规范、算法步骤和验收合同，未编写求解实现，未运行年度优化，也未重做 W1。以下采用用户任务包内 authority；原官方题面全文和 W2 全量数据本轮未提供，不把 authority 转述冒充本轮官方原文核验。

## 1. 必须显式关闭的 S1 冲突

R0《Information and Recourse》第6节允许正常购电即使不用仍付费，剩余供能可存储或 spill。R1《Storage Recourse》第4节却以“无一般 dump-load”的系统为前提，第2.3节称 u 为 PV curtail/spill。

反例：某槽 E=10800、q=100 kWh、L=0、S=0。若 q 全量物理交付、无售电且 0<=u<=S，则平衡要求 100+d=c；SOC 上界要求 eta_c*c<=d/eta_d。在禁止同时充放电时只能 c=d=0，矛盾。取消固定放电也无济于事。即便电池未满，q>L+5000/6 仍可能不可行。这说明“最小 clipping 总能补救”不成立。

本合同推荐 S1-A：**付费 commitment 与物理接收分离**。引入未接收但照付费的正常计划电量 w，0<=w<=q；实际接收 q-w。w 不是售电、不产生收入，也不是免费修改 q。PV 弃光 v 满足 0<=v<=S。R0 的总 spill 用 u=w+v 兼容表示。该解释需要 FYQ/XXT 对正常电量拒收/未利用机制的明确授权，不能静默归类为 R1 已有事实。

若 Controller 明确批准 S1-A，以下数学与实现规则完整可用。若坚持 S1-B（q 必须全部注入，w=0，u<=PV），必须补充可保证吸收的负荷/PV支持集或其他合法出口，并重审风险策略；不得靠提高 epsilon、借 emergency 充电、循环充放电或任意 slack 隐藏 infeasibility。没有支持集时不宣称所有 actual 路径均可行。

这不是已冻结结果的 P0 判决：本轮未发现可核实的 Q2 current implementation 违规。它是数学 release 的证据阻断，必须由 Controller 关闭。

## 2. 索引、单位、输入与已接受边界

日 d、槽 t=1..144，物理区间 (T_d+10(t-1)min,T_d+10t min]。time_mapping_version=`C_R1_RIGHT_ENDPOINT_ORDINAL_EXPORT`。功率 kW 统一除6转槽电量 kWh，价格 p_t 为 CNY/kWh；避免把价格和充电动作都记为 c。

L、S 是实际 load/PV 电量；Lhat、Shat 是当天00:00发出的 point forecast。Q2 p_t **只取附件1固定144槽价格并逐日重复**。W2 dynamic-price行拒绝作为Q2决策或结算输入；consumer_scope=Q4_ONLY。load family=LAG7；PV family=TRAILING7_MEAN。导入前校验非负有限值和完整日槽，不得静默填缺值。

动作 C,D 分别为母线侧充、放电量：0<=C,D<=P=5000/6。SOC 1200<=E<=10800；E'=E+eta_c*C-D/eta_d。primary eta_c=eta_d=0.9，alternative 两者 sqrt(0.9)。无售电、无放电收入；emergency r>=0，其价格是5*p_t，不再额外收一次 p_t*r。

January执行已审R14：q=C=D=0，E=6000；r=max(L-S,0)、v=max(S-L,0)。January仅warm-up，不计正式费用；Feb1初值**读取**Jan31最后槽E，检查为6000，不独立赋初值。正式Feb1–Dec31共334天48096槽；全年Jan–Dec52560槽/52561边界状态。每日E[d,0]=E[d-1,144]，禁止日终复位。

primary terminal=`FREE_BOUNDED_YEAR_END`；12月31日仍只要求SOC界。T1=`EQ_INITIAL_6000`、T2=`GE_INITIAL_6000`为明确附加的敏感性约束。各自全期传播自己的SOC，不拼接不同策略状态。

## 3. 信息时序（Asia/Shanghai）

|阶段|决策时刻|允许新增信息|必须留档|
|---|---|---|---|
|日初预测|T_d 00:00|已发布历史、上一日终SOC、固定tariff|forecast issue/known_at、历史截止、source hash|
|正常购电锁定|T_d，事件序号1|当天forecast、过去残差|144槽q及commitment_hash|
|本槽实现|tau[d,t]，事件序号0|本槽L,S，前槽E|actual_available_at、slot_id|
|储能决策|tau[d,t]，事件序号1|当前及过去actual；未来只用当日冻结forecast|action输入依赖、policy/version|
|应急/余量处理|tau[d,t]，事件序号2|已决定C,D与q、本槽L,S|r,w,v及独立残差|
|状态更新|tau[d,t]，事件序号3|本槽动作|E_before/E_after|

在此离散控制假设中，槽平均actual在右端点可得，并允许用于**本槽**平衡；不声称它在左端点已被预知。这是R1明确的离散实时假设，非对真实在线10分钟控制的无条件保证。若系统只能在槽结束后执行下一槽动作，必须另立延迟控制敏感性，不能倒填 known_at。

同一午夜先完成上日slot144状态更新，再发下一日预测/锁定。普通历史可以 known_at<=T_d；风险残差额外要求 target_ts<T_d（W2 strict cutoff），因此恰在T_d结束的残差不纳入当日风险校准。同一timestamp的顺序用event_sequence审计。

future forecast更新规则固定为 `FROZEN_DAILY_0000`：本日未来槽不更新、不用事后修正forecast；仅当前槽替换actual。明日00:00自然重新预测。动作依赖中的未来forecast target_time可以晚于决策，但其known_at必须不晚于决策。

## 4. Point-forecast日前基线（条件 S1-A）

策略ID=`POINT_DA_LP_R1`。输入为144槽Lhat,Shat,p、当日真实E0、terminal mode。在00:00解以下144槽连续LP：变量 q_t,Cref_t,Dref_t,Eref_t,vref_t>=0，Eref有容量界；

min J_DA=sum_t p_t*q_t；
q_t+Shat_t+Dref_t=Lhat_t+Cref_t+vref_t；
0<=vref_t<=Shat_t；SOC递推及P界如上；Eref_0=当前E0。

日前不设emergency变量，预测净缺口均由正常q覆盖。不设每天E144=E0，不借用Q1日终equality。在12月31日才按T1/T2增加相应预测终端约束。平常日末无salvage value、无额外库存奖励。这是**每日24h截断策略**，末日之外也可能有短视效应；不称全年全局最优。下游须检查每日末段/次日首段应急及SOC，必要时另提延长预测时域合同，不偷偷加入次日actual或重复日终目标。

第一阶段Jstar后，第二阶段min sum(Cref+Dref)，约束J_DA<=Jstar+eps，eps=max(1e-4 CNY,1e-9*abs(Jstar))。该epsilon是本合同明示的数值择优规则，不是风险偏好，不能失败后扩大；精确最优成本和导出方案成本分字段。第二阶段若仍有多解，固定求解器版本/排序；需要平台无关规范解时按(q1..q144,C1..,D1..)依次lexicographic最小化于前述最优面，记录此模式，不偷偷加权。

在正价格、允许PV弃光、eta_c*eta_d<1条件下，可消除同时充放电：取delta=min(C,D/(eta_c*eta_d))，令C'=C-delta，D'=D-eta_c*eta_d*delta，SOC不变、净需求下降；减少q，不足部分增加PV弃光，仍非负且上界允许。因此无需将Q1 MILP裁决直接外推为证明；Q2自己的执行动作仍必须互斥。若数值输出C,D同时大于能量容差，禁止导出，执行上述守SOC修正后重算费用/平衡/Stage2，或报solver异常，不默默截断。

锁定第二阶段的q，并保存(Cref,Dref,Eref)参考计划。日内只能调整storage，不能改q；正常费用按完整q计，不按接收量计。

## 5. CAUSAL_INTRADAY：剩余当日确定性LP

策略ID=`Q2_RH_FIXED_Q_LP_R1`。每槽一次，范围j=t..144，只实施最前一个动作。

令当前j=t用实际L,S，未来j>t用当日00:00冻结Lhat,Shat；q_j全部固定。定义a_j=q_j+S_j-L_j（这里用于规划的L,S按前述组合），常数A_j=max(a_j,0)、B_j=max(-a_j,0)。变量C_j,D_j,r_j,u_j,E_j满足：

0<=C_j<=min(P,A_j)，0<=D_j<=min(P,B_j)；
r_j-u_j=C_j-D_j-a_j，r_j,u_j>=0；
SOC递推及上下界，初值E[t-1]为当前真实状态。

目标min sum_{j=t..144}5*p_j*r_j。正常费用是固定常数，记录但不重复优化。第二阶段在该目标eps内min sum(C+D)，同上数值规则。此**净余量/缺口模式限制**是策略类定义：余量槽只充电，缺口槽只放电，自动杜绝同时C/D与emergency充电；不宣称它包含所有可想象的最优控制。单独的未来变量是预测调度，不是提前执行。

实施动作后独立计算 b=q+S+D-L-C；r=max(-b,0)、u=max(b,0)，再按 v=min(S,u)、w=u-v 分解（PV优先弃、其次拒收已付款normal）；上述模式约束保证0<=w<=q、0<=v<=S。严格禁止直接照抄solver r/u作为实测结算。r>tol时C=0且u=0；无需“有电就最大放电”，允许因后续forecast风险保留SOC。E'=E+eta_c*C-D/eta_d，推进下一槽。

普通主模式下零storage是显式可行fallback：C=D=0、r=max(L-q-S,0)、u=max(q+S-L,0)，同上分解；E不变。仅适用于已批准S1-A。当前数据非法/缺失则 STOP_DATA，不虚构actual。求解失败记录status/runtime，执行fallback并标记degraded；失败率和成本单列，未解释solver failure不得授予优化质量PASS。

T1/T2在12月31日剩余时域LP加入E144目标。预测可达不保证实际可达：未来正常q已锁定、emergency不准充电，故禁止宣称该终端目标总能完成。LP infeasible时输出当前可达上下界/IIS，不放宽终端；为保持物理系统运行可执行零storagefallback，但整条敏感性run标 `FAIL_TERMINAL_OR_REACHABILITY`，不能报告为成功的T1/T2成本对照。S1-A下固定q未来最大可充=min(P,A)，最大可放=min(P,B)，通过界限传播可给终端可达区间。最后槽必须直接检查，禁止跨至2026补电。后续若终端目标经常不可达，另提日前保障机制及已知支持集合同，本版不以future actual规划补救。

## 6. 固定储能必要对照

统一规范名 `DAY_AHEAD_FIXED_STORAGE_WITH_SAFETY_OVERRIDE`；兼容 authority 名 `DAY_AHEAD_FIXED_WITH_SAFETY_OVERRIDE` / `DAY_AHEAD_FIXED_STORAGE_WITH_FEASIBILITY_OVERRIDE`，导出只用规范名，并保留alias字段。

每槽从当日锁定的Cref,Dref出发，令a=q+S-L。若Cref>0，C=min(Cref,P,max(a,0),(10800-E)/eta_c)，D=0；若Dref>0，D=min(Dref,P,max(-a,0),eta_d*(E-1200))，C=0；都为0则保持0。先验证参考动作互斥；不允许把负界剪成正值，不允许增加原动作、改变时段或改方向。由此得到在该方向可行区间内离原指令最近的动作，clipped_charge=Cref-C、clipped_discharge=Dref-D。r/u/w/v与SOC按第5节独立重算。

这是baseline的模式安全投影，不与recourse混名。若S1-B且a-C+D>S，STOP_UNABSORBABLE_COMMITMENT，不虚构dump。T1/T2实际终端不满足仍报FAIL，不强行追加充电。

比较分两层：①政策全期比较各自传播SOC、各自用同一日前规划模型产生q；②隔离储能价值的受控比较共享预先记录的完整q序列，分别传播SOC，不在某日重置使状态相同。不能同时声称全年每个q相同又让两个run用不同E0重新规划。输出明确 comparison_design，前者是整体政策效果，后者是给定commitment下recourse效果。

## 7. Risk-aware候选及评价

只设计一个risk-aware候选 `SIGNED_RESIDUAL_Q80_MARGIN_R1`，完整参数协议见专件。使用过去的**有符号**净负荷残差80%分位，对point净负荷做非负reserve增量，再调用第4节相同日前LP；日内共用第5节或第6节controller。不是把正残差子样本P80直接加入。

正式费用C=sum_{Feb-Dec,t}(p_t*q_dt+5*p_t*r_dt)；正常计划即使拒收仍全额收费。另报January诊断费用但不混入formal总计。报告normal/emergency电量及费用、发生槽/天、P95日应急费用、最大日费用、v与w分别总量、总spill、throughput、全轨迹和终态。日尾部指标用nearest-rank经验分位，零应急日必须保留。

至少 point×{causal,fixed}、risk×{causal,fixed} 在primary efficiency/T0跑满正式期；point+causal与risk+causal各增E2、T1、T2单因素全期run。受控同q储能对照另存报告。新增风险策略须从Jan31真实bridge起传播，不与point互借SOC。

## 8. 数值与质量等级

独立验收能量tol=1e-6 kWh；总成本tol=max(1e-5 CNY,1e-9*abs(recomputed_cost))。元数据、q锁定hash、日期槽完整性、信息来源为严格检查，不能借数值tol放行。累积SOC必须从原初值重建，并报告最大轨迹偏差；实际约束超tol即FAIL。secondary cap只留8 ULP浮点余量，不叠加年度成本tol。

本合同不授予Q2结果数学PASS。仅通过物理/因果复算可称FEASIBLE；优于baseline需完整对照才能称COMPETITIVE；每槽LP最优不等于全年随机控制最优，NEAR-OPTIMAL必须另有适配的有效bound。W2全年残差和Q1结果只作既有诊断背景。

## 9. 手算验收锚点

单位锚点：600 kW持续10min=100 kWh。收费锚点：p=1、q=100、L=150、S=0、D=20、C=0，则r=30，费用=100+5*30=250，SOC减20/0.9；不得计280。

无emergency充电：q=0,S=0,L=50,E=1200，则C=D=0,r=50，不准借r提高E。溢出锚点：第1节反例S1-A取w=100,r=v=C=D=0、收费100*p；S1-B不可行。安全clip锚点：Cref=100,a=30,E=10800时实际C=0，clip=100，u=30；绝不扩大D。终端锚点：最后槽E=1200、a<=0且T1要求6000，则不可达，不能以emergency充电伪造T1 PASS。
