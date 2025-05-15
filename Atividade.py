
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY_NEWS") #Buscar chave Api da file ".env"

if not api_key: #Tratamento de erro para caso não tenha uma chave api
    raise ValueError("API key não encontrada nas variáveis de ambiente!")

def buscar_noticia(tema, quantidade): #Função para o usário buscar o tema da notícia
    '''
    Requisita a a API da "NewsApi" e devolve a lista de notícias
    Headers para declarar chave API
    Params para definir as notícias por tema, por quatidade de páginas, por língua e por notícias mais recentes
    Condição para verificar se o tema é existente na API
    "Articles" é um objeto do Response Object da documentação da API que retorna os resultados da request
    :return:
    '''

    url = "https://newsapi.org/v2/everything"  # Url da API

    headers = { #Declarar chave API
        'X-Api-Key': api_key
    }

    params = {  # Parâmetros da notícia para tema, páginas, língua e notícias mais recentes
        'q': tema,
        'pageSize': quantidade,
        'language': "pt",
        'sortBy': "publishedAt"
    }

    resposta = requests.get(url=url, params=params, headers=headers) #Juntar todas as informações de busca da API
    if resposta.status_code != 200: #Condição para que seja um tema existente na API
        print(f"Erro na API (status {resposta.status_code}).")
        return []
    return resposta.json().get("articles", [])

def exibir_noticias(noticias): #Função para mostrar as notícias
    '''
    Mostra as notícias encontradas
    Laço for para enumerar as notícias e orgazinar por título, fonte e autor
    :return:
    '''

    for i, noticia in enumerate(noticias, 1): #Enumerar as notícias e orgazinar por título, fonte e autor
        print(f"\nNotícia {i}:")
        print("Título:", noticia.get("title", "Sem Título"))
        print("Fonte:", noticia.get("source", {}).get("name", "Desconhecida"))
        print("Autor:", noticia.get("author", "Desconhecido"))

def menu(): #Menu principal do progama
    '''
    Função, menu principal do promagama
    Lista "historico" para guardar os temas
    Contador de notícias
    Laço para mostrar opções do menu e verificar a opção
    Verificar tema e quantidade
    :return:
    '''

    historico = []
    total_noticias = 0

    while True: #Laço para mostrar opções do menu e verificar a opção
        print("\n1. Buscar notícias")
        print("2. Sair")

        opcao = input("Escolha uma opção:")

        if opcao == "1": #Condição para caso opção 1
            tema = input("Digite o tema da notícia: ")
            if not tema: #Condição caso não tenha o tema
                print("Tema não pode estar vazio.")
                continue

            try: #Tentativa de um input da quantidade
                quantidade = int(input("Quantas notícias deseja ver (1 a 20)? "))
            except ValueError: #Condição para retornar erro de valor
                print("Digite um número válido.")
                continue

            # Ajusta limite da quantidade
            if quantidade < 1:
                quantidade = 1
            if quantidade > 20:
                quantidade = 20

            noticias = buscar_noticia(tema, quantidade)
            if noticias:
                print(f"\n {len(noticias)} notícias encontradas para '{tema}'.")
                exibir_noticias(noticias)
                historico.append(tema)
                total_noticias += len(noticias)
            else:
                    print(f"\n Nenhuma notícia retornada para '{tema}'.")

        elif opcao == "2":
            print("\nResumo da sessão:")
            print("Temas buscados:", historico)
            print("Total de buscas:", len(historico))
            print("Total de notícias:", total_noticias)
            break

        else:
            print("Opção inválida. Digite 1 ou 2.")


# chamada direta, sem guard
menu()






