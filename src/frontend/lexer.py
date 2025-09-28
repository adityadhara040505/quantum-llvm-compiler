# Small lexer stub (kept for extensibility). We rely on qiskit.qasm3 for parsing,
# but a custom lexer could be implemented here if needed.
def tokenize_qasm(source: str):
    # Extremely simple whitespace splitting; placeholder
    return source.replace('(', ' ( ').replace(')', ' ) ').split()
