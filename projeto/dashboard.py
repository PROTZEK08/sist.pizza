from flask import render_template
import pickle
import os
from collections import defaultdict
from datetime import datetime

ARQUIVO_PEDIDOS = "pedidos.pkl"


def carregar_pedidos():
    try:
        if os.path.exists(ARQUIVO_PEDIDOS):
            with open(ARQUIVO_PEDIDOS, "rb") as f:
                return pickle.load(f)
    except Exception as e:
        print(f"Erro ao carregar pedidos: {e}")
    return []


def dashboard():
    pedidos = carregar_pedidos()

    qtd_por_item = defaultdict(int)
    valor_por_item = defaultdict(float)
    qtd_por_status = defaultdict(int)
    pedidos_por_garcom = defaultdict(int)
    pedidos_por_dia = defaultdict(int)

    faturamento_total = 0.0
    total_pedidos = len(pedidos)
    total_itens_vendidos = 0

    for pedido in pedidos:
        faturamento_total += pedido.get("total", 0) or 0
        qtd_por_status[pedido.get("status", "Indefinido")] += 1
        pedidos_por_garcom[pedido.get("garcom", "Indefinido")] += 1

        data_hora = pedido.get("data_hora", "")
        dia = data_hora.split("T")[0] if data_hora else "Indefinido"
        pedidos_por_dia[dia] += 1

        for item in pedido.get("itens", []):
            nome_prato = item.get("prato", "Item desconhecido")
            quantidade = item.get("quantidade", 0) or 0
            preco_unitario = item.get("preco_unitario", 0) or 0

            qtd_por_item[nome_prato] += quantidade
            valor_por_item[nome_prato] += quantidade * preco_unitario
            total_itens_vendidos += quantidade

    # ordenar itens pela quantidade vendida (do mais pro menos pedido)
    itens_ordenados = sorted(qtd_por_item.items(), key=lambda x: x[1], reverse=True)
    nomes_itens = [nome for nome, _ in itens_ordenados]
    quantidades_itens = [qtd for _, qtd in itens_ordenados]
    valores_itens = [round(valor_por_item[nome], 2) for nome in nomes_itens]

    prato_mais_vendido = nomes_itens[0] if nomes_itens else "—"
    prato_mais_lucrativo = max(valor_por_item.items(), key=lambda x: x[1])[0] if valor_por_item else "—"
    ticket_medio = (faturamento_total / total_pedidos) if total_pedidos else 0

    # ordenar dias cronologicamente
    dias_ordenados = sorted(pedidos_por_dia.items())
    labels_dias = [d for d, _ in dias_ordenados]
    valores_dias = [q for _, q in dias_ordenados]

    return render_template(
        "dashboard/index.html",
        nomes_itens=nomes_itens,
        quantidades_itens=quantidades_itens,
        valores_itens=valores_itens,
        labels_status=list(qtd_por_status.keys()),
        valores_status=list(qtd_por_status.values()),
        labels_garcom=list(pedidos_por_garcom.keys()),
        valores_garcom=list(pedidos_por_garcom.values()),
        labels_dias=labels_dias,
        valores_dias=valores_dias,
        faturamento_total=round(faturamento_total, 2),
        total_pedidos=total_pedidos,
        total_itens_vendidos=total_itens_vendidos,
        ticket_medio=round(ticket_medio, 2),
        prato_mais_vendido=prato_mais_vendido,
        prato_mais_lucrativo=prato_mais_lucrativo,
    )
