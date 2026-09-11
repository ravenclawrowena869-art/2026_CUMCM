# Official wording excerpt used for S1 adjudication

Source: official `C题.pdf`
SHA256: `2c098f6ae9dd47ae965aebdec3b9facf3de6c173f999783c1012c08fc5fb9d2d`

Q2 relevant wording:

“若每天的电价相同，而小区负载和光伏发电功率随时间变化，且微网提供的电能不可低于小区负载，如果低于负载，需向外网紧急购电，其电价是交易时刻电价的5倍。除紧急购电费用外，其他时间段的购电费用均按计划购电量计算。请在每天0:00制定微网当天的计划购电策略。”

Use:
- exact official wording supports cost accounting by planned amount;
- handling of over-committed but unused normal energy is not explicitly specified, therefore S1-A remains a modeling-completion assumption.
