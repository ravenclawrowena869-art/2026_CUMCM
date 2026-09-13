import argparse
import matplotlib.pyplot as plt
from _common import load_table, require, save_all


def main():
    ap = argparse.ArgumentParser(description='Q2 frozen-data heatmap template; does not fabricate data.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--mode', choices=['emergency', 'pv_bias'], required=True)
    ap.add_argument('--date-col', default='date')
    ap.add_argument('--slot-col', default='slot')
    ap.add_argument('--value-col', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    df = load_table(a.input)
    require(df, [a.date_col, a.slot_col, a.value_col])
    agg = 'sum' if a.mode == 'emergency' else 'mean'
    pivot = df.pivot_table(index=a.date_col, columns=a.slot_col, values=a.value_col, aggfunc=agg)
    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(pivot.to_numpy(), aspect='auto', origin='lower')
    ax.set_xlabel('Time slot')
    ax.set_ylabel('Date index')
    ax.set_title('Emergency purchase heatmap' if a.mode == 'emergency' else 'PV forecast bias heatmap')
    fig.colorbar(im, ax=ax, label=a.value_col)
    fig.tight_layout()
    save_all(fig, a.out)


if __name__ == '__main__':
    main()
