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
