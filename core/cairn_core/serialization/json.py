from __future__ import annotations

import json
from dataclasses import is_dataclass, asdict
from typing import Any, Dict, List

from .errors import SerializationError


def _normalize(obj: Any) -> Any:
    """
    Convert supported objects into JSON-serializable primitives.

    Determinism rules:
    - dict keys must be strings (JSON requirement) and will be sorted at dump-time.
    - tuples are converted to lists, preserving order.
    - dataclasses become dicts recursively.
    - unsupported types raise SerializationError.
    """
    # None/bool/int/float/str are JSON-native
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj

    # dataclasses
    if is_dataclass(obj):
        # asdict() is deterministic given deterministic field order,
        # but we still recursively normalize to enforce type constraints.
        return _normalize(asdict(obj))

    # dict
    if isinstance(obj, dict):
        out: Dict[str, Any] = {}
        for k, v in obj.items():
            if not isinstance(k, str):
                raise SerializationError(
                    "json_key_not_string",
                    f"JSON object keys must be strings; got key type {type(k)!r}",
                )
            out[k] = _normalize(v)
        return out

    # list / tuple
    if isinstance(obj, (list, tuple)):
        return [_normalize(x) for x in obj]

    raise SerializationError(
        "json_unsupported_type",
        f"Object of type {type(obj)!r} is not JSON-serializable",
    )


def to_json_dict(obj: Any) -> Any:
    """
    Public API: normalize to JSON-safe python structures.
    """
    return _normalize(obj)


def to_json_str(obj: Any) -> str:
    """
    Deterministic JSON string.
    """
    normalized = _normalize(obj)
    return json.dumps(
        normalized,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ) + "\n"


def to_json_bytes(obj: Any) -> bytes:
    """
    Deterministic UTF-8 bytes.
    """
    return to_json_str(obj).encode("utf-8")
