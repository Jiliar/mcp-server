# Copilot Instructions for AI Coding Agents

## Project Overview
- This project is a FastMCP server for managing personal expenses (gastos).
- Main entry point: `main.py`.
- Data is stored in a CSV file at `data/gastos.csv`.
- The server exposes tools and resources using the MCP SDK (see `mcp` usage in `main.py`).

## Key Components
- `main.py`: Defines all MCP tools/resources/prompts. Example tools:
  - `agregar_gasto`: Adds a new expense to `data/gastos.csv`.
  - `obtener_gastos`: Returns all expenses as a list of dicts (JSON-like), suitable for LLMs.
- Data schema for each expense: `{fecha, categoria, cantidad, metodo_pago}`.
- Decorators like `@mcp.tool`, `@mcp.resource`, and `@mcp.prompt` are used to expose functions to the MCP server.

## Patterns & Conventions
- Use `csv.DictReader`/`DictWriter` for reading/writing expenses.
- All new expenses are appended to `data/gastos.csv`.
- Dates are handled as `YYYY-MM-DD` strings or Python `datetime` objects.
- Functions are documented with pydoc-style docstrings.
- Error handling: Functions return error messages as strings if exceptions occur.

## Developer Workflows
- To run the server: `python main.py` (ensure the correct virtual environment is activated).
- No tests or build scripts are present by default.
- Add new tools/resources by defining a function and decorating it with the appropriate `@mcp.*` decorator.
- The server port is passed as a string to `FastMCP`.

## Integration & Extensibility
- The project depends on `fastmcp` and `mcp` (see `pyproject.toml`).
- Data is not persisted in a database; all state is in `data/gastos.csv`.
- To add new data fields, update both the CSV and the code that reads/writes it.

## Example: Adding a Tool
```python
@mcp.tool
def mi_funcion(param1: str):
    """Descripción de la función."""
    # lógica aquí
    return resultado
```

## Key Files
- `main.py`: All logic and server setup
- `data/gastos.csv`: Expense data

---
If you add new tools/resources, document their schema and usage here for future agents.
