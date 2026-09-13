import argparse
import matplotlib.pyplot as plt
from _common import load_table, require, save_all


def main():
    ap = argparse.ArgumentParser(description='Q3 stage-ablation plot from frozen annual summary.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--stage-col', default='stage_set')
    ap.add_argument('--cost-col', required=True)
    ap.add_argument('--risk-col', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    df = load_table(a.input)
    require(df, [a.stage_col, a.cost_col, a.risk_col])
    fig, axs = plt.subplots(2, 1, figsize=(8, 7), sharex=True)
    axs[0].bar(df[a.stage_col], df[a.cost_col])
    axs[0].set_ylabel(a.cost_col)
    axs[1].bar(df[a.stage_col], df[a.risk_col])
    axs[1].set_ylabel(a.risk_col)
    axs[1].set_xlabel('Stage set')
    fig.tight_layout()
    save_all(fig, a.out)


if __name__ == '__main__':
    main()
