import argparse
import matplotlib.pyplot as plt
from _common import load_table, require, save_all


def main():
    ap = argparse.ArgumentParser(description='Q3 multivintage mechanism plot from frozen stage ledger.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--time-col', default='time')
    ap.add_argument('--forecast-cols', nargs='+', required=True)
    ap.add_argument('--commitment-cols', nargs='+', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    df = load_table(a.input)
    require(df, [a.time_col, *a.forecast_cols, *a.commitment_cols])
    fig, axs = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    for c in a.forecast_cols:
        axs[0].plot(df[a.time_col], df[c], label=c)
    for c in a.commitment_cols:
        axs[1].plot(df[a.time_col], df[c], label=c)
    axs[0].set_ylabel('Forecast')
    axs[1].set_ylabel('Commitment')
    axs[1].set_xlabel('Time')
    axs[0].legend()
    axs[1].legend()
    fig.tight_layout()
    save_all(fig, a.out)


if __name__ == '__main__':
    main()
