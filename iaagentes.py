import random
from datetime import datetime, timedelta

class AgenteComprador:
    def __init__(self, estoque, demanda, capacidade_estoque, orçamento):
        self.estoque = estoque
        self.demanda = demanda
        self.capacidade_estoque = capacidade_estoque
        self.orçamento = orçamento

    def decidir_compras(self):
        compras = []
        for produto in self.estoque:
            falta = max(self.demanda.get(produto['produto'], 0) - produto['quantidade'], 0)
            if falta > 0:
                if produto['custo'] * falta <= self.orçamento and produto['quantidade'] + falta <= self.capacidade_estoque:
                    compras.append({
                        "produto": produto['produto'],
                        "quantidade": falta,
                        "custo_total": produto['custo'] * falta
                    })
        return compras

class AgenteVendedor:
    def __init__(self, estoque):
        self.estoque = estoque

    def sugerir_promocoes(self):
        promocoes = []
        hoje = datetime.now()
        for produto in self.estoque:
            validade = hoje + timedelta(days=produto['validade'])
            if validade < hoje + timedelta(days=7):  # Produtos próximos ao vencimento
                desconto = round(produto['custo'] * 0.5, 2)
                promocoes.append({
                    "produto": produto['produto'],
                    "desconto": desconto,
                    "quantidade": produto['quantidade']
                })
        return promocoes

class AgentePrevisor:
    def __init__(self, historico_demandas):
        self.historico_demandas = historico_demandas

    def prever_demanda(self):
        previsao = {}
        for produto, historico in self.historico_demandas.items():
            try:
                # Convertendo os valores do histórico para inteiros antes de somar
                historico_int = [int(d) for d in historico[-3:]]  # Garantir que sejam inteiros
                previsao[produto] = int(sum(historico_int) / 3)  # Média dos últimos 3 meses
            except ValueError:
                print(f"Erro ao converter valores para inteiros no histórico de {produto}")
                previsao[produto] = 0  # Se houver erro, atribui 0 como previsão
        return previsao

# Função para rodar a interface
def rodar_interface():
    # Dados de exemplo para os agentes
    estoque = [
        {"produto": "Produto A", "quantidade": 10, "custo": 5.0, "validade": 10},
        {"produto": "Produto B", "quantidade": 20, "custo": 3.0, "validade": 5},
        {"produto": "Produto C", "quantidade": 5, "custo": 8.0, "validade": 20}
    ]
    
    demanda = {
        "Produto A": 15,
        "Produto B": 25,
        "Produto C": 10
    }

    historico_demandas = {
        "Produto A": [12, 14, 10, 15],
        "Produto B": [20, 18, 25, 22],
        "Produto C": [5, 7, 6, 9]
    }

    capacidade_estoque = 50
    orçamento = 100.0
    
    # Criando os agentes
    comprador = AgenteComprador(estoque, demanda, capacidade_estoque, orçamento)
    vendedor = AgenteVendedor(estoque)
    previsor = AgentePrevisor(historico_demandas)

    # Executando as decisões dos agentes
    print("\n--- Decisão de Compras do Agente Comprador ---")
    compras = comprador.decidir_compras()
    for compra in compras:
        print(f"Produto: {compra['produto']}, Quantidade: {compra['quantidade']}, Custo Total: {compra['custo_total']}")

    print("\n--- Sugestões de Promoções do Agente Vendedor ---")
    promocoes = vendedor.sugerir_promocoes()
    for promocao in promocoes:
        print(f"Produto: {promocao['produto']}, Desconto: {promocao['desconto']}, Quantidade: {promocao['quantidade']}")

    print("\n--- Previsões de Demanda do Agente Previsor ---")
    previsoes = previsor.prever_demanda()
    for produto, previsao in previsoes.items():
        print(f"Produto: {produto}, Previsão de Demanda: {previsao}")

if __name__ == "__main__":
    rodar_interface()
