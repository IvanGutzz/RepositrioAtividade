
import requests
import json


#"Banco De Dados" dos usuários
usuarios = {
    "001": {"email": "ana@email.com", "senha": "1234"},
    "002": {"email": "joao@email.com", "senha": "abcd"},
    "003": {"email": "maria@email.com", "senha": "senha123"}
}


#Puxar o banco de usuários
from usuarios import usuarios


#Função para fazer login
def login():
    print("=== LOGIN ===")
    codigo = input("Digite seu código de usuário: ")
    email = input("Digite seu e-mail: ")
    senha = input("Digite sua senha: ")

    if codigo in usuarios:
        dados = usuarios[codigo]
        if dados["email"] == email and dados["senha"] == senha:
            print("Login realizado com sucesso!")
            return codigo  # retorna o código do usuário logado
        else:
            print("E-mail ou senha incorretos.")
    else:
        print("Usuário não encontrado.")

    return None


#Parte principal do programa
usuario_logado = None

while not usuario_logado:
    usuario_logado = login()


#Função do Menu Principal
def menu_principal():
    print("\n=== MENU PRINCIPAL ===")
    print("1 - Visualizar todos os posts")
    print("2 - Visualizar comentários de um post")
    print("3 - Ver meus próprios posts")
    print("4 - Filtrar posts por outro usuário")
    print("5 - Criar novo post")
    print("0 - Sair")

#Guardar resumo das interações, contador
resumo = {
    "posts_visualizados": 0,
    "comentarios_visualizados": 0,
    "posts_criados": 0
}

opcao = None

#Loop para escolha da opção
while opcao != "0":
    menu_principal()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        print("Você escolheu: Visualizar todos os posts")
        # funcionalidade será feita depois
    elif opcao == "2":
        print("Você escolheu: Visualizar comentários de um post")
    elif opcao == "3":
        print("Você escolheu: Ver meus próprios posts")
    elif opcao == "4":
        print("Você escolheu: Filtrar posts por outro usuário")
    elif opcao == "5":
        print("Você escolheu: Criar novo post")
    elif opcao == "0":
        print("Saindo... resumo das interações:")
        print(resumo)
    else:
        print("Opção inválida.")


#Função da opção 1
def listar_todos_os_posts():
    print("\n--- Lista de Posts ---")
    url = "https://jsonplaceholder.typicode.com/posts"
    resposta = requests.get(url)  #Requisição do URL
    if resposta.status_code == 200:  #Condicional de sucesso
        posts = resposta.json()  #Converter Json para dicionário
        for post in posts[:5]:  #Mostrar só os 5 primeiros
            print(f"\nID: {post['id']}")
            print(f"Título: {post['title']}")
            print(f"Conteúdo: {post['body']}")
    else:
        print("Erro ao acessar a API.")

#Opção 1
listar_todos_os_posts()
resumo["posts_visualizados"] += 1


#Função para opção 2
def ver_comentarios_do_post():
    print("\n--- Comentários de um Post ---")
    post_id = input("Digite o ID do post: ")

    url = f"https://jsonplaceholder.typicode.com/comments?postId={post_id}" #*Uso da Query String
    resposta = requests.get(url)

    if resposta.status_code == 200:
        comentarios = resposta.json()
        if comentarios:
            for c in comentarios:
                print(f"\nComentário de: {c['email']}")
                print(f"Mensagem: {c['body']}")
        else:
            print("Nenhum comentário encontrado para esse post.")
    else:
        print("Erro ao acessar a API.")

#Opção 2
ver_comentarios_do_post()
resumo["comentarios_visualizados"] += 1


#userId da API para código do sistema
mapa_usuarios_api = {
    "001": 1,
    "002": 2,
    "003": 3
}

#Função para mostrar posts do usuário logado
def ver_meus_posts(user_code):
    user_id = mapa_usuarios_api.get(user_code) #Variável definida como os códigos salos do sistema

    if not user_id:
        print("Usuário não tem ID correspondente na API.")
        return

    url = f"https://jsonplaceholder.typicode.com/posts?userId={user_id}"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        posts = resposta.json()
        print(f"\n--- Seus Posts ({len(posts)} encontrados) ---")
        for p in posts:
            print(f"\nID: {p['id']}")
            print(f"Título: {p['title']}")
            print(f"Conteúdo: {p['body']}")
    else:
        print("Erro ao acessar a API.")

#Opção 3
ver_meus_posts(usuario_logado)
resumo["posts_visualizados"] += 1



#Função para opção 4
def ver_posts_de_outro_usuario():
    print("\n--- Filtrar posts por outro usuário ---")
    user_id = input("Digite o userId (número de 1 a 10): ")

    if not user_id.isdigit() or not (1 <= int(user_id) <= 10):
        print("ID inválido. Deve ser um número entre 1 e 10.")
        return

    url = f"https://jsonplaceholder.typicode.com/posts?userId={user_id}"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        posts = resposta.json()
        print(f"\n--- Posts do usuário {user_id} ---")
        for p in posts[:5]:
            print(f"\nID: {p['id']}")
            print(f"Título: {p['title']}")
            print(f"Conteúdo: {p['body']}")
    else:
        print("Erro ao acessar a API.")

#Chamar dentro do menu
ver_posts_de_outro_usuario()
resumo["posts_visualizados"] += 1


#Função para opção 5
def criar_novo_post(user_code):
    user_id = mapa_usuarios_api.get(user_code)
    if not user_id:
        print("Usuário não tem ID correspondente na API.")
        return

    print("\n--- Criar novo post ---")
    titulo = input("Digite o título do post: ")
    conteudo = input("Digite o conteúdo do post: ")

    novo_post = { #Dicionário para guardar novo post
        "userId": user_id,
        "title": titulo,
        "body": conteudo
    }

    url = "https://jsonplaceholder.typicode.com/posts"
    resposta = requests.post(url, json=novo_post)

    if resposta.status_code == 201:  #Condição para afirmação da criação
        resultado = resposta.json()
        print("\nPost criado com sucesso (simulado)!")
        print(f"ID: {resultado['id']}")
    else:
        print("Erro ao criar o post.")

#Chamar dentro do menu
criar_novo_post(usuario_logado)
resumo["posts_criados"] += 1


#Função para opção 0
def salvar_resumo(codigo_usuario, dados):
    registro = {
        "usuario": codigo_usuario,
        "resumo": dados
    }

    try:
        with open("historico.json", "a", encoding="utf-8") as arquivo: #"a" para adicionar novas linhas sem apagar anteriores
            json.dump(registro, arquivo) #Grava resumo do arquivo
            arquivo.write("\n")  #Escreve uma linha por vez
        print("Resumo salvo em historico.json.")
    except Exception as e:
        print("Erro ao salvar o arquivo:", e)

#Chamar bloco de saída
salvar_resumo(usuario_logado, resumo)



