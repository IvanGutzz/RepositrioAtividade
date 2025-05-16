
# 1. imports_e_globais.py
import os                                    # Operações de sistema (arquivos, variáveis de ambiente)
import requests                              # Fazer requisições HTTP à API
from dotenv import load_dotenv               # Carregar .env com variáveis de ambiente

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Constantes e variáveis de escopo global
API_KEY = os.getenv("API_KEY_NEWS")          # Chave da NewsAPI
BASE_URL = "https://newsapi.org/v2/everything"
LANGUAGE = "pt"
MAX_PAGE_SIZE = 20
MIN_PAGE_SIZE = 1

if not API_KEY:
    raise ValueError("API key não encontrada nas variáveis de ambiente!")


def buscar_noticias(tema, quantidade):
    """
    Busca notícias recentes na NewsAPI com base no tema e na quantidade informada.

    Parâmetros:
    - tema (str): palavra-chave da busca
    - quantidade (int): número de notícias desejadas (limite entre 1 e 20)

    Retorna:
    - Lista de dicionários contendo as notícias
    """
    # Garantir que a quantidade esteja dentro dos limites
    if quantidade < MIN_PAGE_SIZE:
        quantidade = MIN_PAGE_SIZE
    elif quantidade > MAX_PAGE_SIZE:
        quantidade = MAX_PAGE_SIZE

    # Parâmetros da busca
    parametros = {
        'q': tema,
        'pageSize': quantidade,
        'language': LANGUAGE,
        'sortBy': 'publishedAt'
    }

    # Cabeçalho com a chave da API
    cabecalho = {
        'X-Api-Key': API_KEY
    }

    # Fazer a requisição
    resposta = requests.get(BASE_URL, params=parametros, headers=cabecalho)

    # Verificar se a requisição deu certo
    if resposta.status_code != 200:
        print(f"Erro: código {resposta.status_code}")
        return []

    # Pegar as notícias da resposta
    dados = resposta.json()
    return dados.get("articles", [])


def exibir_noticias(lista_de_noticias):
    """
    Exibe as notícias na tela com título, fonte e autor.

    Parâmetros:
    - lista_de_noticias (list): lista de dicionários retornados da API
    """
    if not lista_de_noticias:
        print("Nenhuma notícia para exibir.")
        return

    for i, noticia in enumerate(lista_de_noticias, start=1):
        print(f"\nNotícia {i}:")
        print("Título:", noticia.get("title", "Sem título"))
        print("Fonte:", noticia.get("source", {}).get("name", "Fonte desconhecida"))
        print("Autor:", noticia.get("author", "Autor desconhecido"))


def menu():
    """
    Exibe o menu principal do programa.
    Permite buscar notícias e mostra um resumo ao final.
    """
    historico_de_temas = []
    total_de_noticias = 0

    while True:
        print("\n=== MENU ===")
        print("1. Buscar notícias")
        print("2. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            tema = input("Digite o tema da notícia: ").strip()
            if not tema:
                print("⚠️ Tema não pode estar vazio.")
                continue

            try:
                quantidade = int(input("Quantas notícias deseja ver (1 a 20)? "))
            except ValueError:
                print("⚠️ Digite um número válido.")
                continue

            noticias = buscar_noticias(tema, quantidade)
            if noticias:
                exibir_noticias(noticias)
                historico_de_temas.append(tema)
                total_de_noticias += len(noticias)
            else:
                print("Nenhuma notícia encontrada.")

        elif opcao == "2":
            print("\n=== RESUMO DA SESSÃO ===")
            print("Temas buscados:", historico_de_temas)
            print("Total de buscas:", len(historico_de_temas))
            print("Total de notícias:", total_de_noticias)
            break

        else:
            print("⚠️ Opção inválida. Escolha 1 ou 2.")

if __name__ == "__main__":
    print("Bem-vindo ao buscador de notícias!")
    menu()

