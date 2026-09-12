# Python Engineering Resources

A phased, self-directed curriculum tracing the path from core language mechanics to applied, production-oriented Python engineering. Each phase is an isolated, runnable artifact — the repository as a whole documents the *reasoning* behind each construct, not just its syntax.

The guiding principle throughout: **every abstraction is chosen because of a trade-off it resolves**, not because it is idiomatic for its own sake. Where a simpler primitive (a function, a dict, a plain loop) would suffice, it is used in preference to a heavier one (a class, a generator, a custom exception).

---

## Repository Structure

```
Python_Resources/
├── phase2.py     # Functional decomposition & parameter design
├── phase3.py     # Iterator protocol, generators, lazy evaluation
├── phase4/       # Package architecture (models / services / utils)
│   ├── main.py
│   ├── models/
│   ├── services/
│   └── utils/
├── phase5.py     # Object-oriented design: composition vs. inheritance
├── phase6.py     # Exception strategy & propagation
├── phase7.py     # Structured data I/O (CSV, JSON, JSONL, encoding)
├── phase8.py     # Environment isolation & dependency management
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

---

## Phase Notes

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

---

## Cross-Cutting Themes

| Theme | Where it shows up |
|---|---|
| Lazy evaluation over eager materialization | Phase 3 generators, Phase 7 JSONL |
| Explicit dependency direction | Phase 4 package layering |
| Composition over inheritance, used judiciously | Phase 5 |
| Fail loud, log with context, handle at the right layer | Phase 6 |
| No implicit platform behavior (always specify) | Phase 7 encoding, Phase 8 pinned versions |

---

## Running the Code

Single-file phases run directly:
```bash
python phase2.py
python phase3.py
python phase5.py
python phase6.py
python phase7.py
python phase8.py
```

Phase 4 is a package and must be run as a module from the parent directory:
```bash
python -m phase4.main
```

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
 