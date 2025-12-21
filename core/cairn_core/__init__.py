"""
Cairn Core

The Cairn Core package contains the security-critical engine for Cairn, including:
- project creation/loading/validation
- authentication and session lifecycle
- cryptography boundaries
- policy evaluation
- annotations and audit logging

UI layers should treat this package as the authoritative source of truth for
security, policy, and project decisions.
"""

from __future__ import annotations

__all__ = ["__version__"]

# Package version. Keep in sync with core/pyproject.toml.
__version__ = "0.1.0"
