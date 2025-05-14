
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY_NEWS")

if not api_key:
    raise ValueError("API key não encontrada nas variáveis de ambiente!")


def menu(): #Mostrar Menu
    print("\n Menu de Opções:")
    print("""
     0 - Sair
     1 - Consultar uma Notícia
     """)

def buscar_noticia(): #Função para o usário buscar o tema da notícia
    '''
    Laço para checkar a existência da notícia
    Buscar notícia
    :return:
    '''
    
    while True: #Laço para buscar uma notícia existente
        noticia_usuario = input("Digite um tema de notícia para buscar: ") #Input do usuário para busca

        url = "https://newsapi.org/v2/everything" #Url da API

        headers = {
        'X-Api-Key': api_key
        }

        params = { #Parâmetros para buscar
        'q': noticia_usuario,
        'language': "pt",
        }

        resposta = requests.get(url=url, params=params, headers=headers)
        resposta_json = resposta.json()
        status_code = resposta.status_code
        print(status_code)
        print(resposta_json)
        if status_code == 200:
            return resposta_json
        else:
            print("Erro")
            break


buscar_noticia()


#while True: #Código principal
    #menu() #Printar o menu





