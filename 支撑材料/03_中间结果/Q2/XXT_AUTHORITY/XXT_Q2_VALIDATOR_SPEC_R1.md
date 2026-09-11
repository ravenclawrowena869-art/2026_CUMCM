Q2_MATH_CONTRACT_ID = CUMCM2026_C_Q2_MATH_CONTRACT_R1

# 独立 validator specification R1

验收器从磁盘source/forecast/commitment/action/settlement/manifest独立读取，禁止复用优化器矩阵或照抄solver PASS。每项输出 status、max_violation、argmax_date/slot、violation_count、first_failure、expected/actual；缺失证据返回INCOMPLETE不返回PASS。

|编号|独立检查|失败行为|
|---|---|---|
|V01|合同ID精确一致，manifest内容hash、S1 authorization存在；无MISSING sentinel|正式run拒绝启动|
|V02|Jan–Dec52560槽年度坐标及Feb-Dec48096正式槽、连续600秒、每自然日144槽；kW/6|FAIL_DATA|
|V03|每日日初q向量hash、sourceforecast hash、形成时间；每槽执行q和最终结算q与承诺逐字节同源|任何免费重规划FAIL|
|V04|所有action输入的known_at<=decision_time；current actual只能在当前right endpoint引入，所有future actual禁止|FAIL_LEAKAGE|
|V05|future forecast为当日00:00snapshot，current实际替换只作用本槽；source dependency全量可追溯|FAIL_LEAKAGE|
|V06|p_t来自Attachment1固定曲线，全部334天逐槽相等；Q2未消费W2动态price|FAIL_PRICE_SOURCE|
|V07|E0读取R14桥；每槽独立递推E'=E+eta_c*C-D/eta_d，跨日无reset；另从Jan1独立累积重建|FAIL_PHYSICS|
|V08|1200..10800容量、C,D<=5000/6、非负有限、无同时C/D；实际C<=max(q+S-L,0)、D<=max(L-q-S,0)按policy约束|FAIL_PHYSICS/POLICY|
|V09|允许storage动作之后重算r=max(L+C-q-S-D,0)、u=max(q+S+D-L-C,0)|FAIL_SETTLEMENT|
|V10|r>tol => C<=tol且u<=tol；允许保留SOC而非必须最大放电|FAIL_EMERGENCY_CHARGING|
|V11|S1-A下u=w+v、0<=w<=q、0<=v<=S；q-w+r+S+D=L+C+v；无售电收益|FAIL_PHYSICS|
|V12|固定baseline独立按min公式投影、动作不增不换方向；逐槽clip及总计/比率|FAIL_BASELINE|
|V13|T0年末仅bounds；T1abs(Eend-6000)、T2max(6000-Eend,0)；不可行敏感性不得伪标PASS|FAIL_TERMINAL|
|V14|正式C=sum(p*q+5*p*r)，分别重算正常费/应急费；January excluded；w不退款|FAIL_ACCOUNTING|
|V15|family=PREDECLARED_BASELINE，W1 Aug-Oct仅offline audit；训练/选择cutoff无回填|FAIL_PROVENANCE|
|V16|每个risk quantile全量重建有符号same-slot历史、strict cutoff、rank、margin；不读取全年positive P80|FAIL_RISK_PROVENANCE|
|V17|solver statuses/gap/runtime/epsilon原值；fallback次数、类型、实际动作验证；无擅自放宽|FAIL_NUMERICAL或DEGRADED|
|V18|纸面指定日期/连续emergency区间按physical boundaries与ordinal export生成，模板文字不驱动solver|FAIL_MAPPING|

V02全年为Jan1–Dec31总计52560槽（其中January4464，formal48096）。边界状态总数52561；formal状态48097。

能量tol=1e-6kWh；成本tol=max(1e-5,1e-9*abs(C))CNY；time/hash/来源/布尔字段零容忍。比较每槽SOC_start与前槽SOC_end以及独立累积轨迹，禁止局部小残差累积漂移。首个超差和全局最大偏差都记录。费用fsum或等价补偿求和；不提前四舍五入。总spill独立拆解paid-normal未利用与PV弃光；不能把二者一并称“弃光”。

full-period因果审计：逐日截断actual访问器，仅放出当前及历史槽；对同一日前历史构造不同future actual，要求q完全一致；对相同前缀、不同未来后缀，要求当前storage动作完全一致（固定求解器和tie-break）；修改evaluation-only全年残差表，正式q不应变化。端点恰在00:00的残差须被当日strict风险cutoff排除，普通history/bridge仍允许该端点已发布状态。

负例必须覆盖：篡改一槽q、future actual进入风险margin、W2动态price注入、r>0时C>0、夜间把paid spill伪标PV、daily SOC复位、terminal失配、fixed动作增加、full precision把Stage2冒称exact optimum、同一timestamp错误事件顺序。数据缺失、桥丢失、未授权S1-A各自硬失败，不通过mock绕过。

年度输出字段：date/slot/physical_start/end/raw_label/commitment_id/q_received/q_committed/w/v/r/C/D/E_before/E_after/p/cost_normal/cost_emergency/cost_total/storage_recourse_mode/forecast_id/model_family_origin/risk_config_id/all_input_known_at_max/decision_time/event_sequence/fallback_reason/terminal_mode/source_hashes。前述q_received=q_committed-w。每日日前另存144槽reference和原始第一/二阶段目标、epsilon、solver证据；禁止reference与actual trajectory混表。

表3具体日期以官方题面为准，本包未列全表3，实现前必须读取原表并保存日期集合hash，不能仅猜12月21日等例示日期。未有官方Excel模板时可先生产long-form候选，不宣称模板读回PASS。
