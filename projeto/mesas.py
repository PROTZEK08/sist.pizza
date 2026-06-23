from flask import render_template, request, redirect
import pickle
import os
from datetime import datetime

ARQUIVO = "mesas.pkl"


def carregar_dados():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "rb") as arquivo:
            return pickle.load(arquivo)
    return []


def salvar_dados(mesas):
    with open(ARQUIVO, "wb") as arquivo:
        pickle.dump(mesas, arquivo)


def listar_mesas():
    mesas = carregar_dados()
    return render_template("mesas/index.html", mesas=mesas)


def cadastrar_mesa():
    if request.method == "POST":
        mesas = carregar_dados()

        id_mesa = request.form["id"]
        for m in mesas:
            if m["id"] == id_mesa:
                return render_template("mesas/cadastrar.html", erro="ID já cadastrado.")

        mesa = {
            "id":            id_mesa,
            "numero":        request.form["numero"],
            "capacidade":    request.form["capacidade"],
            "status":        "Livre",
            "cliente_atual": "",
            "hora_ocupacao": ""
        }

        mesas.append(mesa)
        salvar_dados(mesas)
        return redirect("/mesas")

    return render_template("mesas/cadastrar.html", erro=None)


def editar_mesa(id_mesa):
    mesas = carregar_dados()

    mesa = None
    for m in mesas:
        if m["id"] == id_mesa:
            mesa = m
            break

    if not mesa:
        return redirect("/mesas")

    if request.method == "POST":
        mesa["numero"]     = request.form["numero"]
        mesa["capacidade"] = request.form["capacidade"]
        mesa["status"]     = request.form["status"]

        salvar_dados(mesas)
        return redirect("/mesas")

    return render_template("mesas/editar.html", mesa=mesa)


def excluir_mesa(id_mesa):
    mesas = carregar_dados()
    novas_mesas = []
    for m in mesas:
        if m["id"] != id_mesa:
            novas_mesas.append(m)
    salvar_dados(novas_mesas)
    return redirect("/mesas")


def ocupar_mesa(id_mesa):
    mesas = carregar_dados()

    mesa = None
    for m in mesas:
        if m["id"] == id_mesa:
            mesa = m
            break

    if not mesa:
        return redirect("/mesas")

    if request.method == "POST":
        mesa["status"]        = "Ocupada"
        mesa["cliente_atual"] = request.form["cliente_atual"]
        mesa["hora_ocupacao"] = datetime.now().strftime("%H:%M - %d/%m/%Y")

        salvar_dados(mesas)
        return redirect("/mesas")

    return render_template("mesas/ocupar.html", mesa=mesa)


def liberar_mesa(id_mesa):
    mesas = carregar_dados()
    for m in mesas:
        if m["id"] == id_mesa:
            m["status"]        = "Livre"
            m["cliente_atual"] = ""
            m["hora_ocupacao"] = ""
            break
    salvar_dados(mesas)
    return redirect("/mesas")
