"""Lossless text serialization and portable file provenance."""
import csv
import json
from hashlib import sha256
from pathlib import Path

STRING_FIELDS={'service_date','raw_time_label','physical_start','physical_end','feature_name','event_time','known_at','decision_time','source','run_id','run_class'}

def file_hash(path):
    return sha256(Path(path).read_bytes()).hexdigest()

def write_json(path,data):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def write_csv(path,rows):
    rows=list(rows)
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with Path(path).open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows({k:format(v,'.17g') if isinstance(v,float) else v for k,v in row.items()} for row in rows)

def read_csv(path):
    with Path(path).open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f))
    for row in rows:
        for k,v in row.items():
            if k=='slot_id':row[k]=int(v)
            elif k not in STRING_FIELDS:row[k]=float(v)
    return rows

def portable_relative_path(root, relative):
    """Resolve POSIX or legacy Windows relative manifest paths safely."""
    root=Path(root).resolve()
    normalized=str(relative).replace('\\','/')
    candidate=(root/Path(*normalized.split('/'))).resolve()
    if not candidate.exists():
        parent=candidate.parent
        suffix=candidate.suffix.casefold()
        matches=[p for p in parent.iterdir() if p.is_file() and suffix and p.suffix.casefold()==suffix]
        if candidate.name!='result1_official.xlsx':
            matches=[p for p in matches if p.name!='result1_official.xlsx']
        if len(matches)==1:
            candidate=matches[0].resolve()
    if not candidate.is_relative_to(root):
        raise ValueError('Unsafe relative path: '+str(relative))
    return candidate

def hashes(root,paths):
    return {p.relative_to(root).as_posix():file_hash(p) for p in sorted(paths) if p.is_file()}
