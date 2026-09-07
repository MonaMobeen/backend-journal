
---

## Phase Index

| Phase | Domain | Core Engineering Internals |
|---|---|---|
| 1 | Language Fundamentals | Correct primitive usage; choosing the right data structure for access pattern and mutability requirements |
| 2 | Function Design | Argument contracts (`*args`/`**kwargs`), scope discipline, type-annotated signatures |
| 3 | Iterators & Generators | Lazy evaluation as a memory-management strategy; the iterator protocol underlying every `for` loop |
| 4 | Package Architecture | Dependency direction between `models`, `services`, and entry points; absolute imports at the boundary, relative imports within a package |
| 5 | Object-Oriented Design | When inheritance is correct vs. when composition avoids a fragile hierarchy; `@classmethod` as an alternative-constructor pattern |
| 6 | Exception Strategy | The distinction between *handling* an error and *re-raising with context*; custom exception types as part of a domain's public contract |
| 7 | I/O & Data Interchange | Context managers as the only acceptable file-handling pattern; JSONL as a streaming-friendly alternative to JSON for large record sets |

---

## Running Any Phase

Phases 1, 2, 3, 5, 6, and 7 are standalone scripts:
 

## Engineering Principles  

- **Explicit over implicit** — every transformation is traceable to a specific, intentional line of code; nothing relies on Python "magic" the reader has to reverse-engineer.
- **Fail loud, fail specific** — exceptions are caught by type, never blanket-suppressed; a silent `except: pass` is treated as a defect, not a shortcut.
- **Memory-aware by default** — where a dataset could scale beyond what fits comfortably in memory, the code path defaults to a generator, not a materialized list.
- **Separation of concerns** — business logic, data shape, and low-level utilities are never mixed in the same module once the codebase outgrows a single script (Phase 4 onward).
- **Progressive, non-regressive complexity** — each phase's code builds on primitives established in the phase before it; nothing introduced early is contradicted later.

---

 