
import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Configurar a exibição do DataFrame no terminal
pd.set_option("display.max_colwidth", 80)
pd.set_option("display.width", 160)

# 1. Localizar o arquivo chat.txt na mesma pasta do Python
pasta_atual = Path(__file__).resolve().parent
caminho_chat = pasta_atual / "chat.txt"

# 2. Ler e separar as mensagens do WhatsApp
mensagens = []

with open(caminho_chat, "r", encoding="utf-8-sig") as arquivo:
    for linha in arquivo:
        linha = linha.strip()

        # Formato: [7/11/26, 10:14:08 AM] Carol: mensagem
        resultado = re.match(
            r"^\[(\d{1,2}/\d{1,2}/\d{2,4}), "
            r"(\d{1,2}:\d{2}:\d{2} [AP]M)\] "
            r"([^:]+): (.*)$",
            linha
        )

        if resultado:
            data, hora, remetente, mensagem = resultado.groups()

            mensagens.append([
                data,
                hora,
                remetente,
                mensagem
            ])

        elif mensagens and linha:
            # Mensagens que continuam em outra linha
            mensagens[-1][3] += "\n" + linha

# 3. Criar o DataFrame com as quatro colunas solicitadas
df = pd.DataFrame(
    mensagens,
    columns=["data", "hora", "remetente", "mensagem"]
)

# Verificar se o arquivo contém mensagens válidas
if df.empty:
    print("Nenhuma mensagem encontrada. Verifique o formato do chat.txt.")
    exit()

# Converter a data do formato americano (mês/dia/ano)
df["data"] = pd.to_datetime(df["data"], format="%m/%d/%y")

# 4. Exibir o DataFrame completo
print("\n===== TABELA COMPLETA DAS CONVERSAS =====")

# max_colwidth limita apenas a exibição, não altera os dados
print(df.to_string(index=False, max_colwidth=80))

# 5. Menu principal
while True:

    print("\n===== ANÁLISE DE WHATSAPP =====")
    print("1 - Resumo das conversas")
    print("2 - Histórico do remetente")
    print("3 - Histograma do remetente")
    print("4 - Gráfico de pizza")
    print("5 - Gráfico de linhas")
    print("0 - Sair")

    opcao = input("\nEscolha uma opção: ")

    # OPÇÃO 1 - Resumo das conversas
    if opcao == "1":

        resumo = df["remetente"].value_counts()

        print("\n===== RESUMO DAS CONVERSAS =====")
        print(resumo.to_string())

    # OPÇÃO 2 - Histórico de um remetente
    elif opcao == "2":

        print("\nRemetentes disponíveis:")
        print(df["remetente"].unique())

        nome = input("\nDigite o nome do remetente: ")

        historico = df[df["remetente"] == nome]

        if historico.empty:
            print("Remetente não encontrado.")
        else:
            print("\n===== HISTÓRICO DO REMETENTE =====")

            # Limitar a largura da mensagem no terminal
            print(historico.to_string(
                index=False,
                max_colwidth=80
            ))

    # OPÇÃO 3 - Histograma de mensagens por dia
    elif opcao == "3":

        print("\nRemetentes disponíveis:")
        print(df["remetente"].unique())

        nome = input("\nDigite o nome do remetente: ")

        historico = df[df["remetente"] == nome]

        if historico.empty:
            print("Remetente não encontrado.")
        else:
            # Contar as mensagens por dia
            por_dia = historico.groupby("data").size()

            # Exibir gráfico de barras com a quantidade diária
            por_dia.plot(kind="bar")

            plt.title(f"Mensagens por dia - {nome}")
            plt.xlabel("Data")
            plt.ylabel("Quantidade de mensagens")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    # OPÇÃO 4 - Gráfico de pizza
    elif opcao == "4":

        # Contar mensagens de cada remetente
        resumo = df["remetente"].value_counts()

        resumo.plot(
            kind="pie",
            autopct="%1.1f%%",
            ylabel=""
        )

        plt.title("Percentual de mensagens por remetente")
        plt.tight_layout()
        plt.show()

    # OPÇÃO 5 - Gráfico de linhas
    elif opcao == "5":

        # Agrupar a quantidade de mensagens por data e remetente
        por_dia = df.groupby(
            ["data", "remetente"]
        ).size().unstack(fill_value=0)

        # Cada remetente terá uma linha de cor diferente
        por_dia.plot(
            kind="line",
            marker="o"
        )

        plt.title("Mensagens ao longo do tempo")
        plt.xlabel("Data")
        plt.ylabel("Quantidade de mensagens")
        plt.legend(title="Remetentes")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # OPÇÃO 0 - Encerrar o programa
    elif opcao == "0":

        print("\nPrograma encerrado.")
        break

    # Tratar opções inválidas
    else:
        print("\nOpção inválida. Tente novamente.")
