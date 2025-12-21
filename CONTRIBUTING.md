# Contributing to Cairn

Thank you for your interest in contributing to Cairn.

Cairn is developer infrastructure software with a strong emphasis on security, correctness, and long-term maintainability. Contributions are welcome, but architectural discipline is required.

---

## Project Philosophy

Before contributing, please understand that Cairn prioritizes:

- Local-first operation
- Explicit project and policy boundaries
- Security-first design
- Clear separation between UI and Core
- Conservative, maintainable growth

Features that compromise these principles are unlikely to be accepted.

---

## Contribution Scope

Appropriate contributions include:
- Bug fixes
- Documentation improvements
- Tests
- Performance improvements
- Refactoring that improves clarity or safety

Large features or new subsystems should be discussed **before** implementation.

---

## Architectural Boundaries

Contributors must respect these boundaries:

- UI code must not implement security logic
- Core code must not depend on UI concerns
- Authentication, cryptography, and policy enforcement must remain centralized
- Plugins must not bypass Core APIs

Pull requests that violate these boundaries may be rejected.

---

## Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make focused, minimal changes
4. Add tests where appropriate
5. Ensure CI passes
6. Submit a pull request with a clear description

---

## Code Style

- Python 3.11+
- Follow formatting and linting enforced by CI
- Avoid unnecessary dependencies
- Prefer clarity over cleverness

---

## Security Issues

Do **not** report security vulnerabilities in public issues.  
See `SECURITY.md` for responsible disclosure instructions.

---

## License

By contributing to Cairn, you agree that your contributions will be licensed under the MIT License.
