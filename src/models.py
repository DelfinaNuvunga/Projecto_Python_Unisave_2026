from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    nome: str
    telefone: str
    email: str = ""
    id: Optional[int] = None


@dataclass
class Servico:
    nome: str
    preco: float
    id: Optional[int] = None


@dataclass
class Marcacao:
    cliente_id: int
    servico_id: int
    data: str
    hora: str
    estado: str = "Agendada"
    id: Optional[int] = None
