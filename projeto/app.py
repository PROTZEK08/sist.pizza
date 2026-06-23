from flask import Flask, render_template, request, redirect
import pickle
import os
from pedidos import *
from clientes import *   # ← agora importa do arquivo correto: clientes.py
from mesas import *
from dashboard import *

app = Flask(__name__)

ARQUIVO = "cardapio.pkl"

def carregar_dados():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "rb") as arquivo:
            return pickle.load(arquivo)
    return []

def salvar_dados(cardapio):
    with open(ARQUIVO, "wb") as arquivo:
        pickle.dump(cardapio, arquivo)

@app.route("/")
def index():
    cardapio = carregar_dados()
    return render_template("cardapio/index.html", pratos=cardapio)

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        cardapio = carregar_dados()
        id_prato = request.form["id"]
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        preco = float(request.form["preco"])
        categoria = request.form["categoria"]
        ingredientes = request.form["ingredientes"].split(",")
        tempo_preparo = int(request.form["tempo_preparo"])
        disponivel = request.form["disponivel"]
        foto = request.form["foto"]
        for prato in cardapio:
            if prato["id"] == id_prato:
                return "Erro: ID já cadastrado!"
        prato = {
            "id": id_prato,
            "nome": nome,
            "descricao": descricao,
            "preco": preco,
            "categoria": categoria,
            "ingredientes": ingredientes,
            "tempo_preparo": tempo_preparo,
            "disponivel": disponivel,
            "foto": foto
        }
        cardapio.append(prato)
        salvar_dados(cardapio)
        return redirect("/")
    return render_template("cardapio/cadastrar.html")

@app.route("/excluir/<id_prato>")
def excluir(id_prato):
    cardapio = carregar_dados()
    novo_cardapio = []
    for prato in cardapio:
        if prato["id"] != id_prato:
            novo_cardapio.append(prato)
    salvar_dados(novo_cardapio)
    return redirect("/")

# rotas de pedidos
app.add_url_rule('/pedidos',                     view_func=listar_pedidos)
app.add_url_rule('/pedidos/cadastrar',           view_func=cadastrar_pedido,  methods=['GET', 'POST'])
app.add_url_rule('/pedidos/editar/<id_pedido>',  view_func=editar_pedido,     methods=['GET', 'POST'])
app.add_url_rule('/pedidos/excluir/<id_pedido>', view_func=excluir_pedido)

# rotas de clientes
app.add_url_rule('/clientes',                      view_func=listar_clientes)
app.add_url_rule('/clientes/cadastrar',            view_func=cadastrar_cliente,  methods=['GET', 'POST'])
app.add_url_rule('/clientes/editar/<id_cliente>',  view_func=editar_cliente,     methods=['GET', 'POST'])
app.add_url_rule('/clientes/excluir/<id_cliente>', view_func=excluir_cliente)

# rotas de mesas
app.add_url_rule('/mesas',                       view_func=listar_mesas)
app.add_url_rule('/mesas/cadastrar',             view_func=cadastrar_mesa,     methods=['GET', 'POST'])
app.add_url_rule('/mesas/editar/<id_mesa>',      view_func=editar_mesa,        methods=['GET', 'POST'])
app.add_url_rule('/mesas/excluir/<id_mesa>',     view_func=excluir_mesa)
app.add_url_rule('/mesas/ocupar/<id_mesa>',      view_func=ocupar_mesa,        methods=['GET', 'POST'])
app.add_url_rule('/mesas/liberar/<id_mesa>',     view_func=liberar_mesa)

# rota do dashboard
app.add_url_rule('/dashboard', view_func=dashboard)

if __name__ == "__main__":
    app.run(debug=True)
