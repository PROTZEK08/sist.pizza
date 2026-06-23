from flask import render_template, request, redirect
import pickle
import os

ARQUIVO = "clientes.pkl"


def carregar_dados():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "rb") as arquivo:
            return pickle.load(arquivo)
    return []


def salvar_dados(clientes):
    with open(ARQUIVO, "wb") as arquivo:
        pickle.dump(clientes, arquivo)


def listar_clientes():
    clientes = carregar_dados()
    return render_template("clientes/index.html", clientes=clientes)


def cadastrar_cliente():
    if request.method == "POST":
        clientes = carregar_dados()

        id_cliente = request.form["id"]
        for c in clientes:
            if c["id"] == id_cliente:
                return render_template("clientes/cadastrar.html", erro="ID já cadastrado.")

        cliente = {
            "id":           id_cliente,
            "nome":         request.form["nome"],
            "telefone":     request.form["telefone"],
            "email":        request.form["email"],
            "cpf":          request.form["cpf"],
            "preferencias": request.form["preferencias"],
            "historico":    []
        }

        clientes.append(cliente)
        salvar_dados(clientes)
        return redirect("/clientes")

    return render_template("clientes/cadastrar.html", erro=None)


def editar_cliente(id_cliente):
    clientes = carregar_dados()

    cliente = None
    for c in clientes:
        if c["id"] == id_cliente:
            cliente = c
            break

    if not cliente:
        return redirect("/clientes")

    if request.method == "POST":
        cliente["nome"]         = request.form["nome"]
        cliente["telefone"]     = request.form["telefone"]
        cliente["email"]        = request.form["email"]
        cliente["cpf"]          = request.form["cpf"]
        cliente["preferencias"] = request.form["preferencias"]

        salvar_dados(clientes)
        return redirect("/clientes")

    return render_template("clientes/editar.html", cliente=cliente)


def excluir_cliente(id_cliente):
    clientes = carregar_dados()
    novos_clientes = []
    for c in clientes:
        if c["id"] != id_cliente:
            novos_clientes.append(c)
    salvar_dados(novos_clientes)
    return redirect("/clientes")
