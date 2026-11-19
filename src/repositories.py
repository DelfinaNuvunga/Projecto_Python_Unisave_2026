from .database import Database


class BaseRepository:
    def __init__(self, database: Database):
        self.database = database


class ClienteRepository(BaseRepository):
    def listar(self):
        with self.database.conectar() as con:
            return con.execute("SELECT id, nome, telefone, email FROM clientes ORDER BY nome").fetchall()

    def adicionar(self, nome, telefone, email):
        with self.database.conectar() as con:
            con.execute("INSERT INTO clientes(nome, telefone, email) VALUES (?, ?, ?)", (nome, telefone, email))

    def remover(self, cliente_id):
        with self.database.conectar() as con:
            con.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))


class ServicoRepository(BaseRepository):
    def listar(self):
        with self.database.conectar() as con:
            return con.execute("SELECT id, nome, preco FROM servicos ORDER BY nome").fetchall()

    def adicionar(self, nome, preco):
        with self.database.conectar() as con:
            con.execute("INSERT INTO servicos(nome, preco) VALUES (?, ?)", (nome, preco))

    def remover(self, servico_id):
        with self.database.conectar() as con:
            con.execute("DELETE FROM servicos WHERE id=?", (servico_id,))


class MarcacaoRepository(BaseRepository):
    def listar(self):
        with self.database.conectar() as con:
            return con.execute("""
                SELECT m.id, c.nome, s.nome, m.data, m.hora, m.estado,
                       c.id, s.id, s.preco
                FROM marcacoes m
                JOIN clientes c ON c.id = m.cliente_id
                JOIN servicos s ON s.id = m.servico_id
                ORDER BY m.data, m.hora
            """).fetchall()

    def adicionar(self, cliente_id, servico_id, data, hora):
        with self.database.conectar() as con:
            con.execute("""
                INSERT INTO marcacoes(cliente_id, servico_id, data, hora)
                VALUES (?, ?, ?, ?)
            """, (cliente_id, servico_id, data, hora))

    def alterar_estado(self, marcacao_id, estado):
        with self.database.conectar() as con:
            con.execute("UPDATE marcacoes SET estado=? WHERE id=?", (estado, marcacao_id))

    def remover(self, marcacao_id):
        with self.database.conectar() as con:
            con.execute("DELETE FROM marcacoes WHERE id=?", (marcacao_id,))
