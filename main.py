import os
import tkinter as tk
from tkinter import filedialog, ttk
import datetime
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import shutil
import tkinter.messagebox as messagebox
import threading  # Importe a biblioteca threading

# Variáveis globais
verificacao_ativa = False

# Variável global para a thread de verificação
verificacao_thread = None

def iniciar_verificacao():
    global verificacao_ativa, verificacao_thread
    verificacao_ativa = True

    # Inicie a verificação em uma nova thread
    verificacao_thread = threading.Thread(target=verificar_periodicamente)
    verificacao_thread.start()

def parar_verificacao():
    global verificacao_ativa, verificacao_thread
    verificacao_ativa = False

    # Aguarde a conclusão da thread de verificação
    if verificacao_thread is not None:
        verificacao_thread.join()

def verificar_periodicamente():
    while verificacao_ativa:
        # Obtenha os caminhos dos diretórios selecionados
        diretorio_origem = entry_origem.get()
        caminho_backup = entry_destino.get()
        nome_cliente = entry_cliente.get()

        # Verifique a pasta de origem para novas imagens
        # Copie e salve as novas imagens na pasta de destino, se houver alguma
        copiar_novas_imagens(diretorio_origem, caminho_backup, nome_cliente)
        time.sleep(10)  # Verifique a cada 10 segundos

def copiar_novas_imagens(diretorio_origem, caminho_backup, nome_cliente):
    # Listar todos os arquivos no diretório de origem
    arquivos = os.listdir(diretorio_origem)

    # Filtrar apenas arquivos de imagem (por extensão)
    extensoes_validas = [".jpg", ".jpeg", ".png"]
    arquivos_imagem = [arquivo for arquivo in arquivos if os.path.splitext(arquivo)[1].lower() in extensoes_validas]

    # Encontrar as imagens que não foram copiadas ainda
    for arquivo in arquivos_imagem:
        caminho_completo = os.path.join(diretorio_origem, arquivo)
        caminho_destino = os.path.join(caminho_backup, nome_cliente, arquivo)

        # Verificar se a imagem já existe no diretório do cliente
        if not os.path.exists(caminho_destino):
            # Copiar a imagem para o diretório do cliente
            os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)
            shutil.copy2(caminho_completo, caminho_destino)
            print(f"Imagem copiada e salva em: {caminho_destino}")

# Variável global para o driver do Selenium
driver = None

# Função para abrir a página da web usando o Selenium
def abrir_pagina_web():
    global driver
    if driver is None:
        driver = webdriver.Chrome()
    driver.get("https://web.whatsapp.com")

    while True:
        try:
            campo_pesquisa = driver.find_element_by_xpath('//div[@contenteditable="true"][@data-tab="3"]')

            if campo_pesquisa.is_displayed():
                print("Login concluído.")
                break
            else:
                time.sleep(2)
        except Exception as e:
            print(f"Erro ao verificar o login: {e}")
            break

    nome_cliente = entry_cliente.get()

    campo_pesquisa.send_keys(nome_cliente)
    campo_pesquisa.send_keys(Keys.RETURN)

# Função para selecionar o diretório
def selecionar_diretorio():
    global caminho_arquivos
    caminho_arquivos = filedialog.askdirectory()
    label_diretorio = tk.Label(root, text="")
    label_diretorio.config(text=caminho_arquivos)

# Função para processar os arquivos
def processar_arquivos():
    global caminho_arquivos
    imagem_de_fundo = Image.open("colorful_galaxy.jpg")
    imagem_de_fundo = imagem_de_fundo.resize((largura_janela, altura_janela), Image.ANTIALIAS)
    foto_de_fundo = ImageTk.PhotoImage(imagem_de_fundo)
    label_fundo = tk.Label(root, image=None)
    label_fundo.config(image=foto_de_fundo)
    label_fundo.image = foto_de_fundo

def copiar_ultima_imagem(diretorio_origem, caminho_backup, nome_cliente):
    # Listar todos os arquivos no diretório de origem
    arquivos = os.listdir(diretorio_origem)

    # Filtrar apenas arquivos de imagem (por extensão)
    extensoes_validas = [".jpg", ".jpeg", ".png"]
    arquivos_imagem = [arquivo for arquivo in arquivos if os.path.splitext(arquivo)[1].lower() in extensoes_validas]

    # Encontrar as imagens que não foram copiadas ainda
    for arquivo in arquivos_imagem:
        caminho_completo = os.path.join(diretorio_origem, arquivo)
        caminho_destino = os.path.join(caminho_backup, nome_cliente, arquivo)

        # Verificar se a imagem já existe no diretório do cliente
        if not os.path.exists(caminho_destino):
            # Copiar a imagem para o diretório do cliente
            os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)
            shutil.copy2(caminho_completo, caminho_destino)
            print(f"Imagem copiada e salva em: {caminho_destino}")
            break  # Sair do loop após copiar a primeira imagem


def selecionar_diretorio_origem():
    diretorio_origem = filedialog.askdirectory()
    entry_origem.delete(0, tk.END)
    entry_origem.insert(0, diretorio_origem)

def selecionar_diretorio_destino():
    diretorio_destino = filedialog.askdirectory()
    entry_destino.delete(0, tk.END)
    entry_destino.insert(0, diretorio_destino)

# Variável global para a imagem de fundo
imagem_de_fundo = None

# Criar uma janela do Tkinter
root = tk.Tk()
root.title("PrisTon Tale EXP")

# Configurar o tamanho da janela e centralizá-la
largura_janela = 400
altura_janela = 600
root.geometry(f"{largura_janela}x{altura_janela}+{root.winfo_screenwidth()//2 - largura_janela//2}+{root.winfo_screenheight()//2 - altura_janela//2}")

# Impedir redimensionamento da janela
root.resizable(False, False)

# Definir uma imagem de fundo
imagem_de_fundo = Image.open("colorful_galaxy.jpg")
imagem_de_fundo = imagem_de_fundo.resize((largura_janela, altura_janela), Image.LANCZOS)
imagem_de_fundo = ImageTk.PhotoImage(imagem_de_fundo)
fundo_label = tk.Label(root, image=imagem_de_fundo)
fundo_label.place(relwidth=1, relheight=1)

# Campo de entrada para o nome do cliente
fonte_cliente = ("Verdana", 14, "bold")  # Escolha a fonte desejada
label_cliente = ttk.Label(root, text="Nome do Cliente:", font=fonte_cliente)
label_cliente.pack(pady=(180, 20))  # Adicione espaço vertical apenas acima do widget

entry_cliente = ttk.Entry(root, font=fonte_cliente)
entry_cliente.pack(pady=5)  # Adicione padding vertical (5 pixels) ao campo de entrada

# Campo de entrada para o diretório de origem
fonte_origem = ("Verdana", 14, "bold")  # Escolha a fonte desejada
label_origem = ttk.Label(root, text="Diretório de Origem:", font=fonte_origem)
label_origem.pack(pady=5)

entry_origem = ttk.Entry(root, font=fonte_origem)
entry_origem.pack(pady=5)  # Adicione padding vertical (5 pixels) ao campo de entrada

button_selecionar_origem = ttk.Button(root, text="Selecionar Origem", command=selecionar_diretorio_origem)
button_selecionar_origem.pack(pady=5)

# Campo de entrada para o diretório de destino
fonte_destino = ("Verdana", 14, "bold")  # Escolha a fonte desejada
label_destino = ttk.Label(root, text="Diretório de Destino:", font=fonte_destino)
label_destino.pack(pady=5)

entry_destino = ttk.Entry(root, font=fonte_destino)
entry_destino.pack(pady=5)  # Adicione padding vertical (5 pixels) ao campo de entrada

button_selecionar_destino = ttk.Button(root, text="Selecionar Destino", command=selecionar_diretorio_destino)
button_selecionar_destino.pack(pady=5)  # Adicione padding vertical (5 pixels) ao botão

# Botão para copiar a imagem mais recente
button_copiar_imagem = ttk.Button(root, text="Copiar Imagem", command=lambda: copiar_ultima_imagem(entry_origem.get(), entry_destino.get(), entry_cliente.get()))
button_copiar_imagem.pack(pady=5)  # Adicione mais padding vertical (10 pixels) ao botão

# Botão para abrir a página da web
button_abrir_pagina = ttk.Button(root, text="Abrir WhatsApp Web e Enviar ao Cliente", command=abrir_pagina_web)
button_abrir_pagina.pack(pady=5)

# Botão para iniciar a verificação
button_iniciar_verificacao = ttk.Button(root, text="Iniciar Verificação", command=iniciar_verificacao)
button_iniciar_verificacao.pack(pady=5)

# Botão para parar a verificação
button_parar_verificacao = ttk.Button(root, text="Parar Verificação", command=parar_verificacao)
button_parar_verificacao.pack(pady=5)


root.mainloop()

