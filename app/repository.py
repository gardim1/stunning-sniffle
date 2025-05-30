"""
estrutura em memoria + persistência simples em JSON.
mantem lista ordenada por timestamp ISO usando bisect (O(log n)).
"""

from bisect import bisect_left, insort
from datetime import datetime
from pathlib import Path
import json
from typing import Dict, List, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIDAS_DIR = BASE_DIR / "data" / "medidas"
MEDIDAS_DIR.mkdir(parents=True, exist_ok=True)

_samples_by_ts: List[Tuple[str, str, Dict]] = []

def _ts() -> str:
    return datetime.now().isoformat(timespec="seconds")


def add_sample(cpf: str, sample: Dict) -> None:
    insort(_samples_by_ts, (_ts(), cpf, sample))

def samples_by_cpf(cpf: str) -> List[Dict]:
    return [s for _, c, s in _samples_by_ts if c == cpf]


def _path_cpf(cpf: str) -> Path:
    return MEDIDAS_DIR / f"{cpf}.json"

def persist_sample(cpf: str, sample: Dict) -> None:
    path = _path_cpf(cpf)
    try:
        dados = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        dados = []
    dados.append(sample)
    path.write_text(json.dumps(dados, indent=4), encoding="utf-8")

def load_samples_from_disk(cpf: str) -> List[Dict]:
    path = _path_cpf(cpf)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))
