import yaml
from typing import Any, Dict


def dump_workflow_yaml(workflow_obj: Dict[str, Any]) -> str:
    return yaml.safe_dump(workflow_obj)


def load_workflow_yaml(yaml_text: str) -> Dict[str, Any]:
    return yaml.safe_load(yaml_text)
