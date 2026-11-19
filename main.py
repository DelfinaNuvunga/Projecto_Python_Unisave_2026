"""
Gestão de Salão UNISAVE
Aplicação desktop desenvolvida em Python com Tkinter para gerir clientes,
serviços e marcações de um salão de beleza utilizando SQLite.
"""

from src.app import SalaoApp


if __name__ == "__main__":
    app = SalaoApp()
    app.run()
