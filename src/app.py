import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from .database import Database
from .repositories import ClienteRepository, ServicoRepository, MarcacaoRepository


class SalaoApp:
    def __init__(self):
        self.database = Database()
        self.database.inicializar()
        self.clientes = ClienteRepository(self.database)
        self.servicos = ServicoRepository(self.database)
        self.marcacoes = MarcacaoRepository(self.database)

        self.root = tk.Tk()
        self.root.title("UniSave — Gestão de Salão")
        self.root.geometry("1120x720")
        self.root.minsize(950, 620)

        cores = {
            "fundo": "#f7f2f5",
            "primaria": "#8a3f70",
            "primaria_escura": "#66304f",
            "rosa": "#e8b7d1",
            "texto": "#3d2935",
        }
        self.root.configure(bg=cores["fundo"])

        estilo = ttk.Style(self.root)
        estilo.theme_use("clam")
        estilo.configure("TFrame", background=cores["fundo"])
        estilo.configure("TLabel", background=cores["fundo"], foreground=cores["texto"], font=("Segoe UI", 10))
        estilo.configure("TEntry", fieldbackground="#ffffff", bordercolor="#d8bdcb", foreground=cores["texto"])
        estilo.configure("TCombobox", fieldbackground="#ffffff", bordercolor="#d8bdcb", foreground=cores["texto"])
        estilo.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(12, 8), foreground="#ffffff", background=cores["primaria"])
        estilo.map("TButton", background=[("active", cores["primaria_escura"]), ("pressed", cores["primaria_escura"])])
        estilo.configure("TNotebook", background=cores["fundo"], borderwidth=0)
        estilo.configure("TNotebook.Tab", font=("Segoe UI", 11, "bold"), padding=(22, 10), background="#eadde4", foreground=cores["texto"])
        estilo.map("TNotebook.Tab", background=[("selected", cores["primaria"])], foreground=[("selected", "#ffffff")])
        estilo.configure("Treeview", font=("Segoe UI", 10), rowheight=34, fieldbackground="#ffffff", background="#ffffff", foreground=cores["texto"])
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background=cores["primaria_escura"], foreground="#ffffff", padding=(8, 8))
        estilo.map("Treeview.Heading", background=[("active", cores["primaria"])])
        
        cabecalho = tk.Frame(self.root, bg=cores["primaria_escura"], height=82)
        cabecalho.pack(fill="x", side="top")
        cabecalho.pack_propagate(False)
        tk.Label(cabecalho, text="UNISAVE", bg=cores["primaria_escura"], fg="#ffffff", font=("Segoe UI", 22, "bold")).pack(side="left", padx=(24, 12), pady=18)
        tk.Label(cabecalho, text="Gestão inteligente do seu salão", bg=cores["primaria_escura"], fg="#f1d7e4", font=("Segoe UI", 11)).pack(side="left", pady=(7, 0))

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=16, pady=(14, 8))

        self.tab_clientes = ttk.Frame(notebook)
        self.tab_servicos = ttk.Frame(notebook)
        self.tab_marcacoes = ttk.Frame(notebook)
        notebook.add(self.tab_clientes, text="Clientes")
        notebook.add(self.tab_servicos, text="Serviços")
        notebook.add(self.tab_marcacoes, text="Marcações")

        self._criar_tabela_clientes()
        self._criar_tabela_servicos()
        self._criar_tabela_marcacoes()
        self._atualizar_todas()

        self.status = tk.Label(
            self.root,
            text="Sistema pronto",
            anchor="w",
            bg="#eadde4",
            fg="#66304f",
            font=("Segoe UI", 9),
            padx=16,
            pady=7,
        )
        self.status.pack(fill="x", side="bottom")

    def run(self):
        self.root.mainloop()

    def _tabela(self, parent, columns, headings, widths):
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True, padx=14, pady=(6, 12))

        tabela = ttk.Treeview(container, columns=columns, show="headings", selectmode="browse")
        for coluna, titulo, largura in zip(columns, headings, widths):
            tabela.heading(coluna, text=titulo)
            tabela.column(coluna, width=largura, anchor="center", minwidth=60)

        scroll = ttk.Scrollbar(container, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=scroll.set)
        tabela.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        tabela.tag_configure("par", background="#ffffff")
        tabela.tag_configure("impar", background="#f5edf2")
        return tabela

    def _criar_tabela_clientes(self):
        form = ttk.Frame(self.tab_clientes)
        form.pack(fill="x", padx=10, pady=8)
        self.cl_nome = tk.StringVar(); self.cl_tel = tk.StringVar(); self.cl_email = tk.StringVar()
        for i, (texto, var) in enumerate((("Nome", self.cl_nome), ("Telefone", self.cl_tel), ("Email", self.cl_email))):
            ttk.Label(form, text=texto).grid(row=0, column=i*2, padx=4)
            ttk.Entry(form, textvariable=var, width=24).grid(row=0, column=i*2+1, padx=4)
        ttk.Button(form, text="Adicionar", command=self._adicionar_cliente).grid(row=0, column=6, padx=8)
        ttk.Button(form, text="Eliminar", command=self._eliminar_cliente).grid(row=0, column=7)

        self.tabela_clientes = self._tabela(self.tab_clientes, ("id", "nome", "telefone", "email"), ("ID", "Nome", "Telefone", "Email"), (50, 220, 150, 230))

    def _adicionar_cliente(self):
        try:
            nome, telefone, email = self.cl_nome.get().strip(), self.cl_tel.get().strip(), self.cl_email.get().strip()
            if not nome or not telefone:
                raise ValueError("Preencha o nome e o telefone.")
            self.clientes.adicionar(nome, telefone, email)
            self.cl_nome.set(""); self.cl_tel.set(""); self.cl_email.set("")
            self._atualizar_clientes(); self._atualizar_comboboxes()
        except (ValueError, Exception) as erro:
            messagebox.showerror("Erro", str(erro))

    def _eliminar_cliente(self):
        item = self.tabela_clientes.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um cliente."); return
        try:
            id_cliente = self.tabela_clientes.item(item[0], "values")[0]
            if messagebox.askyesno("Confirmar", "Eliminar este cliente?"):
                self.clientes.remover(id_cliente)
                self._atualizar_todas()
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def _criar_tabela_servicos(self):
        form = ttk.Frame(self.tab_servicos)
        form.pack(fill="x", padx=10, pady=8)
        self.serv_nome = tk.StringVar(); self.serv_preco = tk.StringVar()
        ttk.Label(form, text="Serviço").grid(row=0, column=0, padx=4)
        ttk.Entry(form, textvariable=self.serv_nome, width=35).grid(row=0, column=1, padx=4)
        ttk.Label(form, text="Preço (MT)").grid(row=0, column=2, padx=4)
        ttk.Entry(form, textvariable=self.serv_preco, width=15).grid(row=0, column=3, padx=4)
        ttk.Button(form, text="Adicionar", command=self._adicionar_servico).grid(row=0, column=4, padx=8)
        ttk.Button(form, text="Eliminar", command=self._eliminar_servico).grid(row=0, column=5)

        self.tabela_servicos = self._tabela(self.tab_servicos, ("id", "nome", "preco"), ("ID", "Serviço", "Preço (MT)"), (50, 300, 150))

    def _adicionar_servico(self):
        try:
            nome = self.serv_nome.get().strip()
            preco = float(self.serv_preco.get().strip())
            if not nome:
                raise ValueError("Preencha o nome do serviço.")
            if preco < 0:
                raise ValueError("O preço não pode ser negativo.")
            self.servicos.adicionar(nome, preco)
            self.serv_nome.set(""); self.serv_preco.set("")
            self._atualizar_servicos(); self._atualizar_comboboxes()
        except ValueError as erro:
            messagebox.showerror("Erro", "Dados inválidos. " + str(erro))
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def _eliminar_servico(self):
        item = self.tabela_servicos.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um serviço."); return
        try:
            id_servico = self.tabela_servicos.item(item[0], "values")[0]
            if messagebox.askyesno("Confirmar", "Eliminar este serviço?"):
                self.servicos.remover(id_servico)
                self._atualizar_todas()
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def _criar_tabela_marcacoes(self):
        form = ttk.Frame(self.tab_marcacoes)
        form.pack(fill="x", padx=10, pady=8)
        self.m_cliente = tk.StringVar(); self.m_servico = tk.StringVar()
        self.m_data = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d")); self.m_hora = tk.StringVar(value="09:00")

        ttk.Label(form, text="Cliente").grid(row=0, column=0, padx=4)
        self.cb_cliente = ttk.Combobox(form, textvariable=self.m_cliente, state="readonly", width=22)
        self.cb_cliente.grid(row=0, column=1, padx=4)
        ttk.Label(form, text="Serviço").grid(row=0, column=2, padx=4)
        self.cb_servico = ttk.Combobox(form, textvariable=self.m_servico, state="readonly", width=22)
        self.cb_servico.grid(row=0, column=3, padx=4)
        ttk.Label(form, text="Data").grid(row=0, column=4, padx=4)
        ttk.Entry(form, textvariable=self.m_data, width=11).grid(row=0, column=5)
        ttk.Label(form, text="Hora").grid(row=0, column=6, padx=4)
        ttk.Entry(form, textvariable=self.m_hora, width=8).grid(row=0, column=7)
        ttk.Button(form, text="Marcar", command=self._adicionar_marcacao).grid(row=0, column=8, padx=8)

        botoes = ttk.Frame(self.tab_marcacoes)
        botoes.pack(fill="x", padx=10)
        ttk.Button(botoes, text="Concluir", command=lambda: self._alterar_estado("Concluída")).pack(side="left", padx=4)
        ttk.Button(botoes, text="Cancelar", command=lambda: self._alterar_estado("Cancelada")).pack(side="left", padx=4)
        ttk.Button(botoes, text="Eliminar", command=self._eliminar_marcacao).pack(side="left", padx=4)

        self.tabela_marcacoes = self._tabela(self.tab_marcacoes, ("id", "cliente", "servico", "data", "hora", "estado", "preco"), ("ID", "Cliente", "Serviço", "Data", "Hora", "Estado", "Preço (MT)"), (50, 170, 170, 110, 90, 120, 100))

    def _adicionar_marcacao(self):
        try:
            if not self.m_cliente.get() or not self.m_servico.get():
                raise ValueError("Selecione cliente e serviço.")
            datetime.strptime(self.m_data.get(), "%Y-%m-%d")
            datetime.strptime(self.m_hora.get(), "%H:%M")
            cliente_id = int(self.cb_cliente["values"][self.cb_cliente.current()].split(" - ")[0])
            servico_id = int(self.cb_servico["values"][self.cb_servico.current()].split(" - ")[0])
            self.marcacoes.adicionar(cliente_id, servico_id, self.m_data.get(), self.m_hora.get())
            self._atualizar_marcacoes()
        except ValueError as erro:
            messagebox.showerror("Erro", "Dados inválidos. " + str(erro))
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def _alterar_estado(self, estado):
        item = self.tabela_marcacoes.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma marcação."); return
        try:
            id_marcacao = self.tabela_marcacoes.item(item[0], "values")[0]
            self.marcacoes.alterar_estado(id_marcacao, estado)
            self._atualizar_marcacoes()
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def _eliminar_marcacao(self):
        item = self.tabela_marcacoes.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma marcação."); return
        try:
            id_marcacao = self.tabela_marcacoes.item(item[0], "values")[0]
            if messagebox.askyesno("Confirmar", "Eliminar esta marcação?"):
                self.marcacoes.remover(id_marcacao)
                self._atualizar_marcacoes()
        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def _atualizar_clientes(self):
        for item in self.tabela_clientes.get_children():
            self.tabela_clientes.delete(item)
        for indice, cliente in enumerate(self.clientes.listar(), start=1):
            tag = "par" if indice % 2 == 0 else "impar"
            self.tabela_clientes.insert("", "end", values=cliente, tags=(tag,))

    def _atualizar_servicos(self):
        for item in self.tabela_servicos.get_children():
            self.tabela_servicos.delete(item)
        for indice, servico in enumerate(self.servicos.listar(), start=1):
            tag = "par" if indice % 2 == 0 else "impar"
            self.tabela_servicos.insert("", "end", values=(servico[0], servico[1], f"{servico[2]:.2f} MT"), tags=(tag,))

    def _atualizar_marcacoes(self):
        for item in self.tabela_marcacoes.get_children():
            self.tabela_marcacoes.delete(item)
        for indice, marcacao in enumerate(self.marcacoes.listar(), start=1):
            tag = "par" if indice % 2 == 0 else "impar"
            self.tabela_marcacoes.insert("", "end", values=(marcacao[0], marcacao[1], marcacao[2], marcacao[3], marcacao[4], marcacao[5], f"{marcacao[8]:.2f} MT"), tags=(tag,))

    def _atualizar_comboboxes(self):
        clientes = [f"{item[0]} - {item[1]}" for item in self.clientes.listar()]
        servicos = [f"{item[0]} - {item[1]}" for item in self.servicos.listar()]
        self.cb_cliente["values"] = clientes
        self.cb_servico["values"] = servicos

    def _atualizar_todas(self):
        self._atualizar_clientes()
        self._atualizar_servicos()
        self._atualizar_marcacoes()
        self._atualizar_comboboxes()
        if hasattr(self, "status"):
            self.status.configure(
                text=(
                    f"{len(self.clientes.listar())} clientes  •  "
                    f"{len(self.servicos.listar())} serviços  •  "
                    f"{len(self.marcacoes.listar())} marcações"
                )
            )


