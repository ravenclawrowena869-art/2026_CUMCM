import argparse
import matplotlib.pyplot as plt
from _common import load_table, require, save_all


def main():
    ap = argparse.ArgumentParser(description='Q4 aligned causal-price / purchase / SOC mechanism panel.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--time-col', default='time')
    ap.add_argument('--price-col', required=True)
    ap.add_argument('--purchase-col', required=True)
    ap.add_argument('--soc-col', required=True)
    ap.add_argument('--emergency-col')
    ap.add_argument('--oracle-price-col', help='Optional diagnostic only; never deployable ranking.')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    df = load_table(a.input)
    cols = [a.time_col, a.price_col, a.purchase_col, a.soc_col]
    if a.emergency_col:
        cols.append(a.emergency_col)
    if a.oracle_price_col:
        cols.append(a.oracle_price_col)
    require(df, cols)
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    axs[0].plot(df[a.time_col], df[a.price_col], label='causal price input')
    if a.oracle_price_col:
        axs[0].plot(df[a.time_col], df[a.oracle_price_col], linestyle='--', label='oracle diagnostic')
    axs[0].set_ylabel('Price')
    axs[0].legend()
    axs[1].plot(df[a.time_col], df[a.purchase_col], label='purchase')
    if a.emergency_col:
        axs[1].plot(df[a.time_col], df[a.emergency_col], label='emergency purchase')
    axs[1].set_ylabel('Purchase')
    axs[1].legend()
    axs[2].plot(df[a.time_col], df[a.soc_col])
    axs[2].set_ylabel('SOC')
    axs[2].set_xlabel('Time')
    fig.tight_layout()
    save_all(fig, a.out)


if __name__ == '__main__':
    main()
