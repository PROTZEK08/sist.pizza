from flask import render_template, request, redirect
import pickle
import os
import json

ARQUIVO_PEDIDOS = "pedidos.pkl"
ARQUIVO_CARDAPIO = "cardapio.pkl"


def carregar_pedidos():
    try:
        if os.path.exists(ARQUIVO_PEDIDOS):
            with open(ARQUIVO_PEDIDOS, "rb") as f:
                return pickle.load(f)
    except Exception as e:
        print(f"Erro ao carregar pedidos: {e}")
    return []


def carregar_cardapio():
    try:
        if os.path.exists(ARQUIVO_CARDAPIO):
            with open(ARQUIVO_CARDAPIO, "rb") as f:
                return pickle.load(f)
    except Exception as e:
        print(f"Erro ao carregar cardápio: {e}")
    return []


def salvar_pedidos(pedidos):
    try:
        with open(ARQUIVO_PEDIDOS, "wb") as f:
            pickle.dump(pedidos, f)
        print(f"✓ Pedidos salvos com sucesso")
    except Exception as e:
        print(f"✗ Erro ao salvar pedidos: {e}")
        raise


def calcular_total(itens):
    return sum(item["quantidade"] * item["preco_unitario"] for item in itens)


def listar_pedidos():
    pedidos = carregar_pedidos()
    status_filtro = request.args.get("status", "")
    if status_filtro:
        pedidos = [p for p in pedidos if p["status"] == status_filtro]
    return render_template("pedidos/index.html", pedidos=pedidos, status_filtro=status_filtro)


def cadastrar_pedido():
    cardapio = carregar_cardapio()

    if request.method == "POST":
        try:
            pedidos = carregar_pedidos()
            id_pedido = request.form["id"].strip()

            # Verificar ID único
            for p in pedidos:
                if p["id"] == id_pedido:
                    return "Erro: ID de pedido já cadastrado!", 400

            itens_json = request.form.get("itens_json", "[]")
            try:
                itens = json.loads(itens_json)
            except json.JSONDecodeError:
                itens = []

            total = calcular_total(itens)

            pedido = {
                "id":            id_pedido,
                "numero_pedido": int(request.form["numero_pedido"]),
                "data_hora":     request.form["data_hora"],
                "mesa":          request.form["mesa"].strip(),
                "cliente":       request.form["cliente"].strip(),
                "garcom":        request.form["garcom"].strip(),
                "status":        request.form["status"],
                "observacoes":   request.form.get("observacoes", "").strip(),
                "itens":         itens,
                "total":         total
            }

            pedidos.append(pedido)
            salvar_pedidos(pedidos)
            return redirect("/pedidos")
        except Exception as e:
            print(f"Erro ao cadastrar pedido: {e}")
            return f"Erro ao cadastrar pedido: {e}", 500

    return render_template("pedidos/cadastrar.html", cardapio=cardapio)


def editar_pedido(id_pedido):
    pedidos = carregar_pedidos()
    cardapio = carregar_cardapio()

    pedido = next((p for p in pedidos if p["id"] == id_pedido), None)
    if not pedido:
        return "Pedido não encontrado!", 404

    if request.method == "POST":
        try:
            itens_json = request.form.get("itens_json", "[]")
            try:
                itens = json.loads(itens_json)
            except json.JSONDecodeError:
                itens = []

            total = calcular_total(itens)

            pedido["numero_pedido"] = int(request.form["numero_pedido"])
            pedido["data_hora"]     = request.form["data_hora"]
            pedido["mesa"]          = request.form["mesa"].strip()
            pedido["cliente"]       = request.form["cliente"].strip()
            pedido["garcom"]        = request.form["garcom"].strip()
            pedido["status"]        = request.form["status"]
            pedido["observacoes"]   = request.form.get("observacoes", "").strip()
            pedido["itens"]         = itens
            pedido["total"]         = total

            salvar_pedidos(pedidos)
            return redirect("/pedidos")
        except Exception as e:
            print(f"Erro ao editar pedido: {e}")
            return f"Erro ao editar pedido: {e}", 500

    return render_template("pedidos/editar.html", pedido=pedido, cardapio=cardapio)


def excluir_pedido(id_pedido):
    try:
        pedidos = carregar_pedidos()
        pedidos = [p for p in pedidos if p["id"] != id_pedido]
        salvar_pedidos(pedidos)
        return redirect("/pedidos")
    except Exception as e:
        print(f"Erro ao excluir pedido: {e}")
        return f"Erro ao excluir pedido: {e}", 500