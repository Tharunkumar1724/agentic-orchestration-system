import yaml
import json
from pathlib import Path
from typing import Any
from enum import Enum

BASE = Path(__file__).resolve().parent.parent / "config"
BASE.mkdir(parents=True, exist_ok=True)

DATA_BASE = Path(__file__).resolve().parent.parent / "data"
DATA_BASE.mkdir(parents=True, exist_ok=True)


def _path_for(kind: str, id: str) -> Path:
    (BASE / kind).mkdir(parents=True, exist_ok=True)
    return (BASE / kind / f"{id}.yaml")


def _data_path_for(kind: str, id: str) -> Path:
    """Get path for JSON copy in data folder."""
    (DATA_BASE / kind).mkdir(parents=True, exist_ok=True)
    return (DATA_BASE / kind / f"{id}.json")


def _convert_enums(obj: Any) -> Any:
    """Recursively convert Enum values to strings for YAML serialization."""
    if isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, dict):
        return {k: _convert_enums(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_enums(item) for item in obj]
    return obj


def save(kind: str, id: str, obj: Any):
    """Save object as YAML file and also JSON copy for workflows."""
    p = _path_for(kind, id)
    # Convert enums to strings before saving
    converted_obj = _convert_enums(obj)
    
    # Save YAML version
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(converted_obj, f, default_flow_style=False, sort_keys=False)
    
    # Also save JSON copy for workflows in data folder
    if kind == "workflows":
        json_path = _data_path_for(kind, id)
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(converted_obj, f, indent=2, default=str)
    
    return str(p)


def load(kind: str, id: str):
    """Load object from YAML file."""
    p = _path_for(kind, id)
    if not p.exists():
        return None
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def list_all(kind: str):
    """List all YAML files in a config category."""
    d = BASE / kind
    if not d.exists():
        return []
    out = []
    for p in d.glob("*.yaml"):
        with p.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data:
                out.append(data)
    return out


def delete(kind: str, id: str) -> bool:
    """Delete a YAML config file and JSON copy if exists."""
    p = _path_for(kind, id)
    deleted = False
    
    if p.exists():
        p.unlink()
        deleted = True
    
    # Also delete JSON copy for workflows
    if kind == "workflows":
        json_path = _data_path_for(kind, id)
        if json_path.exists():
            json_path.unlink()
    
    return deleted
