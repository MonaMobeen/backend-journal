# Python Engineering Resources

A phased, self-directed curriculum tracing the path from core language mechanics to applied, production-oriented Python engineering. Each phase is an isolated, runnable artifact — the repository as a whole documents the *reasoning* behind each construct, not just its syntax.

The guiding principle throughout: **every abstraction is chosen because of a trade-off it resolves**, not because it is idiomatic for its own sake. Where a simpler primitive (a function, a dict, a plain loop) would suffice, it is used in preference to a heavier one (a class, a generator, a custom exception).

---

## Repository Structure

```
Python_Resources/
├── phase1.py                    # Language fundamentals & core data structures
├── phase2.py                    # Functional decomposition & parameter design
├── phase3.py                    # Iterator protocol, generators, lazy evaluation
├── phase4/                      # Package architecture (models / services / utils)
│   ├── main.py
│   ├── models/
│   ├── services/
│   └── utils/
├── phase5.py                    # Object-oriented design: composition vs. inheritance
├── phase6.py                    # Exception strategy & propagation
├── phase7.py                    # Structured data I/O (CSV, JSON, JSONL, encoding)
├── phase8.py                    # Environment isolation & dependency management
├── phase9.py                    # Clean, maintainable Python
├── phase10.py                   # Debugging & structured logging
├── phase11_calculator.py        # Code under test
├── test_phase11_calculator.py   # pytest suite: unit tests, fixtures, mocking
├── phase12.py                   # Functional programming
├── phase13.py                   # Advanced Python: closures, decorators, dunders
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

---

## Phase Notes

### Phase 1 — Language Fundamentals
Primitive types, operators, control flow, and the four core data structures (list, tuple, set, dict), chosen deliberately based on mutability and access-pattern requirements rather than habit.

### Phase 2 — Functional Decomposition
Parameterization strategy is treated as a design decision, not boilerplate: positional vs. keyword arguments, `*args`/`**kwargs` for variadic interfaces, default values, and static type annotations. The trade-off called out explicitly is that variadic signatures (`*args`, `**kwargs`) trade static type-checkability for flexibility — mitigated here via type hints, internal validation, and reserving variadic signatures for genuinely generic call sites (decorators, dispatchers) rather than domain functions.

### Phase 3 — Iterators, Generators & Lazy Evaluation
Implements the iterator protocol manually (`iter()`/`next()`/`StopIteration`) before relying on `for`, to make explicit what the `for` statement abstracts away. Generator functions (`yield`) and generator expressions are used to demonstrate **lazy evaluation** — values are produced on demand rather than materialized eagerly, which is the deciding factor when data volume (large files, unbounded streams) makes full materialization infeasible. Includes a line-by-line file-processing pattern and a chunking utility, both direct precursors to real ETL patterns.

### Phase 4 — Package Architecture
A minimal but real package layout (`models/`, `services/`, `utils/`, entry point at `main.py`) demonstrating both **absolute** imports (used at the composition root, `main.py`) and **relative** imports (used inside the package, `services/user_service.py`). The split enforces a dependency direction: `utils` has no knowledge of `services` or `models`; `services` composes `models` and `utils`; nothing imports `main`. This is the same layering discipline applied in larger service-oriented codebases, just at a scale small enough to read in one sitting.

> Run as a module from one level above the package: `python -m phase4.main` — not `python main.py`. This is intentional: relative imports only resolve when the package is invoked as a module, which is the same constraint you'll hit in any real multi-file Python application.

### Phase 5 — Object-Oriented Design
Covers the standard OOP toolkit (encapsulation via `@property`, inheritance, polymorphism, `@classmethod`/`@staticmethod`, `@dataclass`) with an explicit bias toward **composition over inheritance** where the relationship is "has-a" rather than "is-a" (`Car` *has* an `Engine`; a `Cat` *is* an `Animal`). Also documents the inverse case most tutorials skip: when a plain function or dict is the correct choice over a class, because there is no state to encapsulate and no behavior to attach.

### Phase 6 — Exception Strategy
Goes beyond `try`/`except` mechanics into exception *design*: custom exception types for domain-specific failure modes, propagation across call boundaries, and the log-then-re-raise pattern for separating "where an error is detected" from "where an error is meaningfully handled." Explicitly avoids bare `except:` clauses, which is treated as a correctness issue, not a style preference — silently swallowing unknown exception types hides real defects.

### Phase 7 — Structured Data I/O
Text, CSV, JSON, and JSONL, with `pathlib` for cross-platform path handling and explicit UTF-8 encoding on every file operation (encoding is never left to the platform default). JSONL is used specifically to connect back to Phase 3: it is the on-disk format that pairs naturally with line-by-line generator processing, for the same reason — avoiding full materialization of large datasets.

### Phase 8 — Environment & Dependency Management
Documents `venv` creation/activation and the `requirements.txt` / `pyproject.toml` split: the former as a lockfile-style dependency snapshot, the latter as project metadata and build configuration. The repository is intentionally dependency-free at this stage — `dependencies = []` — since introducing a package before there is a real need for it would misrepresent what the code actually requires.

### Phase 9 — Clean, Maintainable Python
PEP 8 conventions, meaningful naming, single-responsibility functions, DRY principles, constants over magic values, and guard clauses to eliminate deep nesting.

### Phase 10 — Debugging & Logging
Traceback interpretation, `breakpoint()`-driven interactive debugging, call-stack reasoning, and severity-tiered structured logging (`debug` → `critical`).

### Phase 11 — Testing
Unit tests, `pytest` fixtures, parameterized test cases, and mocking external dependencies to isolate units under test. Code under test (`phase11_calculator.py`) and its test suite (`test_phase11_calculator.py`) are kept in separate files, mirroring standard test-discovery conventions.

### Phase 12 — Functional Programming
First-class functions, pure functions, higher-order functions, `map`/`filter`/`reduce`, `lambda`, and `functools.partial`, with an explicit example of favoring named, decomposed steps over a single unreadable chained expression.

### Phase 13 — Advanced Python
Closures, decorators, the context manager protocol (`__enter__`/`__exit__`), and dunder methods (`__repr__`, `__len__`, `__eq__`) for native integration with Python's built-in behaviors (`print()`, `len()`, `==`).

---

## Cross-Cutting Themes

| Theme | Where it shows up |
|---|---|
| Lazy evaluation over eager materialization | Phase 3 generators, Phase 7 JSONL |
| Explicit dependency direction | Phase 4 package layering |
| Composition over inheritance, used judiciously | Phase 5 |
| Fail loud, log with context, handle at the right layer | Phase 6, Phase 10 |
| No implicit platform behavior (always specify) | Phase 7 encoding, Phase 8 pinned versions |
| Readability over cleverness | Phase 9, Phase 12 |

---

## Running the Code

Single-file phases run directly:
```bash
python phase1.py
python phase2.py
python phase3.py
python phase5.py
python phase6.py
python phase7.py
python phase8.py
python phase9.py
python phase10.py
python phase12.py
python phase13.py
```

Phase 4 is a package and must be run as a module from the parent directory:
```bash
python -m phase4.main
```

Phase 11 requires `pytest`:
```bash
pip install pytest --break-system-packages
pytest test_phase11_calculator.py -v
```

---

## Engineering Principles Applied

- **Explicit over implicit** — every transformation is traceable and intentional
- **Memory-aware design** — generator-based lazy evaluation is preferred over eager materialization where scale is a concern
- **Separation of concerns** — logic is decomposed into single-responsibility functions
- **Progressive complexity** — each phase builds directly on primitives established in the previous phase

---

## Reference Resources

- [Python Language Reference](https://docs.python.org/3/reference/) — canonical semantics, not just the tutorial
- [PEP 8](https://peps.python.org/pep-0008/) — style guide
- [PEP 20 — The Zen of Python](https://peps.python.org/pep-0020/)
- [Effective Python (Brett Slatkin)](https://effectivepython.com/) — idiom-level design trade-offs, closely mirrors this repo's phase notes
- [Fluent Python (Luciano Ramalho)](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/) — deep dive on the data model, iterators/generators, and OOP internals
- [Real Python — Iterators and Generators](https://realpython.com/introduction-to-python-generators/)
- [Python Packaging User Guide](https://packaging.python.org/en/latest/)

---
 