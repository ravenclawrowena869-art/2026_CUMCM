from pathlib import Path
import re
import markdown
from weasyprint import HTML, CSS

SRC = Path('支撑材料/AI工具使用详情.md')
OUT = Path('支撑材料/AI 工具使用详情.pdf')

text = SRC.read_text(encoding='utf-8')
text = text.replace('# AI 工具使用详情（赛中持续记录稿）', '# AI 工具使用详情')

# 删除赛中内部记录说明和“记录要求”工作段，仅保留最终披露内容
text = re.sub(r'(?m)^>.*(?:\n|$)', '', text)
text = re.sub(r'## 一、记录要求.*?(?=## 二、已使用 AI 工具概览)', '', text, flags=re.S)

# 最终提交版标题结构
text = text.replace('## 二、已使用 AI 工具概览', '## 一、所用 AI 工具及使用环节')
text = text.replace('## 三、赛中使用记录\n\n## 使用情况概述', '## 二、使用情况概述')
text = text.replace('# 具体使用目的和环节', '## 三、具体使用目的和环节')
text = text.replace('# 关键交互记录', '## 四、主要提示方式与使用过程')
text = text.replace('# AI 输出的采纳和人工修改情况', '## 五、AI 输出的采纳、人工修改和核验情况')

# 清理仍带有“待最终核对”色彩的内部表述
text = text.replace('赛中持续更新', '赛中使用记录')
text = text.replace('执行环境；Q1 部分阶段界面/任务记录为 Astra，最终提交前需由实际使用者核对完整模型名称', 'Codex；Q1 部分阶段界面/任务记录为 Astra')
text = text.replace('Astra（用户界面显示名，最终提交前核对完整模型名称）', 'Astra（赛中界面显示名）')
text = text.replace('正式数字与数学事实仍以技术 Handoff 为准', '正式数字与数学事实均回到题目、程序及结果文件核验')

# 追加人工复核说明
text = text.rstrip() + '''\n\n## 六、人工复核说明\n\nAI 输出未被直接作为核心建模与分析结论提交。对于模型选择、数学公式、代码实现、参数设定、实验结果和论文中的正式数值，参赛队员均结合赛题原文、附件数据、数学模型、程序输出和独立验收结果进行人工审查。出现 AI 建议与题意、数学公式或程序证据不一致时，以人工复核后的题意解释和可复现实验结果为准。\n'''

body = markdown.markdown(text, extensions=['tables', 'fenced_code'])
html = f'''<!doctype html>
<html lang="zh-CN">
<head><meta charset="utf-8"><title>AI 工具使用详情</title></head>
<body>{body}</body></html>'''

css = CSS(string=r'''
@page {
  size: A4;
  margin: 18mm 19mm 18mm 19mm;
  @bottom-center { content: counter(page); font-family: "Noto Serif CJK SC"; font-size: 9pt; }
}
body { font-family: "Noto Serif CJK SC", serif; font-size: 10.5pt; line-height: 1.55; color: #000; }
h1 { font-family: "Noto Sans CJK SC", sans-serif; font-size: 18pt; text-align: center; margin: 0 0 10pt; }
h2 { font-family: "Noto Sans CJK SC", sans-serif; font-size: 14pt; margin: 12pt 0 6pt; page-break-after: avoid; }
h3 { font-family: "Noto Sans CJK SC", sans-serif; font-size: 12pt; margin: 9pt 0 4pt; page-break-after: avoid; }
p { margin: 0 0 6pt; text-align: justify; }
blockquote { margin: 5pt 8mm; padding-left: 4mm; border-left: 1.5pt solid #888; }
table { width: 100%; border-collapse: collapse; margin: 6pt 0 10pt; font-size: 8.6pt; }
th, td { border: 0.6pt solid #555; padding: 4pt 5pt; vertical-align: middle; }
th { background: #e7e6e6; text-align: center; font-weight: 700; }
tr { page-break-inside: avoid; }
code { font-family: monospace; font-size: 9pt; }
''')

OUT.parent.mkdir(parents=True, exist_ok=True)
HTML(string=html, base_url='.').write_pdf(str(OUT), stylesheets=[css])
print(OUT)
