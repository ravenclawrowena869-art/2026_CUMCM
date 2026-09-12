"""Strict, read-only attachment parser. Template display labels never enter here."""
from datetime import time
from hashlib import sha256
import math
from pathlib import Path
import re
import openpyxl

REFERENCE_DATE = '2000-01-01'  # Synthetic coordinate, not an official Q1 date.

def source_workbook(root):
    """Locate the single supplied source workbook without re-encoding its name."""
    files=[p for p in (Path(root)/'source').glob('*.xlsx') if p.name!='result1_official.xlsx']
    if len(files)!=1:
        raise ValueError('Expected exactly one source workbook')
    return files[0]

def clock_label(minutes):
    return f'{minutes//60:02d}:{minutes%60:02d}'

def normalize_rows(values):
    values = list(values)
    if len(values) != 144:
        raise ValueError('Expected exactly 144 input slots')
    rows=[]
    for t, value in enumerate(values, 1):
        if len(value) != 4:
            raise ValueError(f'Slot {t}: expected four source columns')
        stamp, price, load, pv = value
        raw = f'{stamp.hour}:{stamp.minute:02d}' if isinstance(stamp,time) else str(stamp).strip()
        if isinstance(stamp,time) and (stamp.second or stamp.microsecond):
            raise ValueError('Non-ten-minute timestamp')
        match=re.fullmatch(r'(\d{1,2}):(\d{2})(\+1)?', raw)
        if not match:
            raise ValueError(f'Invalid raw timestamp {raw}')
        h,m,day=match.groups(); h=int(h);m=int(m)
        if h>23 or m>59 or (day and (h or m)):
            raise ValueError(f'Invalid raw timestamp {raw}')
        endpoint=h*60+m+(1440 if day else 0)
        if endpoint != t*10:
            raise ValueError(f'Slot {t}: raw endpoint mismatch {raw}')
        for name, x in [('price',price),('load',load),('pv',pv)]:
            if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x):
                raise ValueError(f'Slot {t}: invalid {name}')
        if price<=0 or load<0 or pv<0:
            raise ValueError(f'Slot {t}: nonpositive price or negative power')
        rows.append(dict(slot_id=t,service_date=REFERENCE_DATE,raw_time_label=raw,
                         physical_start=clock_label((t-1)*10),physical_end=clock_label(t*10),
                         dt_hours=1/6,price_yuan_per_kwh=float(price),load_kw=float(load),pv_kw=float(pv),
                         load_kwh=float(load)/6,pv_kwh=float(pv)/6))
    return rows

def parse_source(path):
    path=Path(path);before=sha256(path.read_bytes()).hexdigest()
    wb=openpyxl.load_workbook(path,read_only=True,data_only=True)
    try:
        if len(wb.worksheets)!=1:
            raise ValueError('Unexpected workbook sheet count')
        sheet=wb.worksheets[0]
        values=list(sheet.values)
        if tuple(values[0]) != ('时间','电价','小区负载','光伏发电预测功率'):
            raise ValueError('Unexpected source header')
        rows=normalize_rows(values[1:])
    finally:
        wb.close()
    if sha256(path.read_bytes()).hexdigest()!=before:
        raise RuntimeError('Source changed during parsing')
    return rows
