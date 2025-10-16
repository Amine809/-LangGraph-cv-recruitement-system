"""
Utilities to convert complex Python objects (e.g., LangChain messages) into
JSON-serializable structures for exporting reports and persistence.
"""
from typing import Any, Dict, List
from pathlib import Path
from datetime import datetime, date

try:
    from langchain_core.messages import BaseMessage
except Exception:
    BaseMessage = None  # type: ignore


def _serialize_message(msg: Any) -> Dict[str, Any]:
    """
    Convert a LangChain BaseMessage (e.g., AIMessage, HumanMessage) to a plain dict.
    Falls back to string conversion if BaseMessage is unavailable.
    """
    if BaseMessage is not None and isinstance(msg, BaseMessage):
        result: Dict[str, Any] = {
            "type": getattr(msg, "type", msg.__class__.__name__),
            "content": getattr(msg, "content", None),
        }
        # Optional attributes commonly present on messages
        optional_attrs = ["name", "id", "example", "additional_kwargs", "response_metadata"]
        for attr in optional_attrs:
            if hasattr(msg, attr):
                result[attr] = getattr(msg, attr)
        return result
    # Fallback: best-effort string representation
    return {"type": getattr(msg, "__class__", type(msg)).__name__, "content": str(msg)}


def to_json_safe(obj: Any) -> Any:
    """
    Recursively convert an object into a JSON-serializable structure.
    - LangChain BaseMessage -> dict
    - sets/tuples -> lists
    - datetime/date/Path -> string
    - dict/list -> recursively processed
    - unknown objects -> string representation
    """
    # Base cases for simple types
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj

    # LangChain messages
    if BaseMessage is not None and isinstance(obj, BaseMessage):
        return _serialize_message(obj)

    # Common containers
    if isinstance(obj, dict):
        return {str(k): to_json_safe(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple, set)):
        return [to_json_safe(v) for v in obj]

    # Common non-serializable primitives
    if isinstance(obj, (datetime, date, Path)):
        return str(obj)

    # Fallback: try __dict__ then string
    if hasattr(obj, "__dict__"):
        try:
            return {str(k): to_json_safe(v) for k, v in obj.__dict__.items()}
        except Exception:
            pass

    return str(obj)


