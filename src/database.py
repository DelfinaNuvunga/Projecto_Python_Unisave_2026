import sqlite3
from pathlib import Path


class Database:
    def __init__(self, caminho="data/salao.db"):
        self.caminho = caminho
        Path(caminho).parent.mkdir(parents=True, exist_ok=True)

    def conectar(self):
        return sqlite3.connect(self.caminho)

    def inicializar(self):
        with self.conectar() as conexao:
            conexao.executescript("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    telefone TEXT NOT NULL,
                    email TEXT
                );
                CREATE TABLE IF NOT EXISTS servicos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    preco REAL NOT NULL CHECK(preco >= 0)
                );
                CREATE TABLE IF NOT EXISTS marcacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    servico_id INTEGER NOT NULL,
                    data TEXT NOT NULL,
                    hora TEXT NOT NULL,
                    estado TEXT NOT NULL DEFAULT 'Agendada',
                    FOREIGN KEY(cliente_id) REFERENCES clientes(id),
                    FOREIGN KEY(servico_id) REFERENCES servicos(id)
                );
            """)
            self._adicionar_dados_teste(conexao)

    def _adicionar_dados_teste(self, conexao):
        """Insere dados de demonstração apenas em uma base vazia."""
        if conexao.execute("SELECT COUNT(*) FROM clientes").fetchone()[0] == 0:
            conexao.executemany(
                "INSERT INTO clientes(nome, telefone, email) VALUES (?, ?, ?)",
                (
                    ("Ana Sofia", "+258 84 123 4567", "ana.sofia@exemplo.com"),
                    ("Marta Cossa", "+258 82 234 5678", "marta.cossa@exemplo.com"),
                    ("Beatriz Mondlane", "+258 87 345 6789", "beatriz@exemplo.com"),
                    ("Joana Almeida", "+258 86 456 7890", "joana@exemplo.com"),
                    ("Cláudia Tomás", "+258 84 567 8901", "claudia@exemplo.com"),
                ),
            )

        if conexao.execute("SELECT COUNT(*) FROM servicos").fetchone()[0] == 0:
            conexao.executemany(
                "INSERT INTO servicos(nome, preco) VALUES (?, ?)",
                (
                    ("Corte feminino", 650.0),
                    ("Penteado", 850.0),
                    ("Manicure", 450.0),
                    ("Pedicure", 550.0),
                    ("Maquilhagem", 1200.0),
                    ("Tratamento capilar", 950.0),
                ),
            )

        if conexao.execute("SELECT COUNT(*) FROM marcacoes").fetchone()[0] == 0:
            primeiro_cliente = conexao.execute("SELECT id FROM clientes ORDER BY id LIMIT 1").fetchone()
            primeiro_servico = conexao.execute("SELECT id FROM servicos ORDER BY id LIMIT 1").fetchone()
            if primeiro_cliente and primeiro_servico:
                hoje = __import__("datetime").date.today().isoformat()
                conexao.execute(
                    "INSERT INTO marcacoes(cliente_id, servico_id, data, hora, estado) VALUES (?, ?, ?, '09:30', 'Agendada')",
                    (primeiro_cliente[0], primeiro_servico[0], hoje),
                )
