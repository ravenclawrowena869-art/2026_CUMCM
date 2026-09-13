from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def load_table(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    if p.suffix.lower() in {'.xlsx', '.xls'}:
        return pd.read_excel(p)
    if p.suffix.lower() == '.csv':
        return pd.read_csv(p)
    raise ValueError('input must be .csv/.xlsx/.xls')


def require(df, cols):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise KeyError(f'missing columns: {missing}')


def save_all(fig, out: str):
    p = Path(out)
    p.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(p.with_suffix('.png'), dpi=300, bbox_inches='tight')
    fig.savefig(p.with_suffix('.pdf'), bbox_inches='tight')
