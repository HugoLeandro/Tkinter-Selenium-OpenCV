import os
import tkinter as tk
from tkinter import filedialog, ttk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import shutil
import tkinter.messagebox as messagebox
import threading  # Importe a biblioteca threading
from datetime import datetime

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
    imagem_de_fundo = Image.open("pristontale_01.jpg")
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

    # Inicialize variáveis para rastrear a imagem mais recente
    imagem_mais_recente = None
    data_hora_imagem_mais_recente = None

    # Encontrar a imagem mais recente com base na data e hora de modificação
    for arquivo in arquivos_imagem:
        caminho_completo = os.path.join(diretorio_origem, arquivo)

        # Obtenha a data e hora de modificação do arquivo
        data_hora_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_completo))

        # Verifique se esta é a imagem mais recente
        if imagem_mais_recente is None or data_hora_modificacao > data_hora_imagem_mais_recente:
            imagem_mais_recente = arquivo
            data_hora_imagem_mais_recente = data_hora_modificacao

    if imagem_mais_recente is not None:
        caminho_destino = os.path.join(caminho_backup, nome_cliente, imagem_mais_recente)

        # Verificar se a imagem já existe no diretório do cliente
        if not os.path.exists(caminho_destino):
            # Copiar a imagem para o diretório do cliente
            os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)
            shutil.copy2(os.path.join(diretorio_origem, imagem_mais_recente), caminho_destino)
            print(f"Imagem copiada e salva em: {caminho_destino}")
        else:
            messagebox.showinfo("Imagem Existente", f"A última imagem com a data e hora mais recente já está na pasta de destino: {caminho_destino}")
    else:
        messagebox.showinfo("Sem Imagens", "Não foram encontradas imagens no diretório de origem.")




def selecionar_diretorio_origem():
    diretorio_origem = filedialog.askdirectory()
    entry_origem.delete(0, tk.END)
    entry_origem.insert(0, diretorio_origem)

def selecionar_diretorio_destino():
    diretorio_destino = filedialog.askdirectory()
    entry_destino.delete(0, tk.END)
    entry_destino.insert(0, diretorio_destino)

# Função para atualizar o estado dos botões
def atualizar_estado_botao(botao):
    if botao == "Iniciar":
        iniciar_verificacao()
    elif botao == "Parar":
        parar_verificacao()

# Variável global para a imagem de fundo
imagem_de_fundo = None

root = tk.Tk()
root.title("PrisTon Tale EXP")

# Configurar o tamanho da janela e centralizá-la
largura_janela = 800
altura_janela = 600
root.geometry(f"{largura_janela}x{altura_janela}+{root.winfo_screenwidth()//2 - largura_janela//2}+{root.winfo_screenheight()//2 - altura_janela//2}")

# Impedir redimensionamento da janela
root.resizable(False, False)

# Definir uma imagem de fundo
imagem_de_fundo = Image.open("pristontale_01.jpg")
imagem_de_fundo = imagem_de_fundo.resize((largura_janela, altura_janela), Image.LANCZOS)
imagem_de_fundo = ImageTk.PhotoImage(imagem_de_fundo)
fundo_label = tk.Label(root, image=imagem_de_fundo)
fundo_label.place(relwidth=1, relheight=1)

# Criar um estilo personalizado para os botões
style = ttk.Style()

# Variável para rastrear o estado dos botões
estado_botao = tk.StringVar()

# Criar um Frame para os botões "Iniciar Verificação" e "Parar Verificação"
frame_botoes = ttk.Frame(root)
frame_botoes.pack(side="top", anchor="w", padx=10, pady=10)  # Posicione o frame na parte superior esquerda com padding

# Radiobutton para iniciar a verificação
radiobutton_iniciar = ttk.Radiobutton(frame_botoes, text="Iniciar Verificação", variable=estado_botao, value="Iniciar", command=lambda: atualizar_estado_botao("Iniciar"))
radiobutton_iniciar.pack(side="left", padx=(10, 0), pady=10, anchor="w")  # Adicione padx esquerda (10) e remova o padx direita (0)

# Radiobutton para parar a verificação
radiobutton_parar = ttk.Radiobutton(frame_botoes, text="Parar Verificação", variable=estado_botao, value="Parar", command=lambda: atualizar_estado_botao("Parar"))
radiobutton_parar.pack(side="left", padx=(10, 0), pady=10, anchor="w")  # Adicione padx esquerda (10) e remova o padx direita (0)

# Crie um frame com fundo #014C69
frame = tk.Frame(root, bg="#014C69")
frame.pack(padx=10, pady=10, anchor="w")  # Adicione anchor="w"

# Campo de entrada para o nome do cliente
fonte_cliente = ("Verdana", 14, "bold")
label_cliente = ttk.Label(frame, text="Nome do Cliente:", font=fonte_cliente)

# Defina a cor de fundo da etiqueta (label) para #014C69
label_cliente.configure(background="#014C69")

# Defina a cor do texto para branco (#FFFFFF)
label_cliente.configure(foreground="#FFFFFF")

label_cliente.pack(pady=(10, 5))  # Reduza o pady inferior para 5

entry_cliente = ttk.Entry(frame, font=fonte_cliente)
entry_cliente.pack(pady=5, anchor="w")  # Adicione anchor="w"

# Campo de entrada para o diretório de origem
fonte_origem = ("Verdana", 14, "bold")  # Escolha a fonte desejada
label_origem = ttk.Label(frame, text="Diretório de Origem:", font=fonte_origem)

# Defina a cor de fundo da etiqueta (label) para #014C69
label_origem.configure(background="#014C69")

# Defina a cor do texto para branco (#FFFFFF)
label_origem.configure(foreground="#FFFFFF")

label_origem.pack(pady=(10, 10), padx=(30, 0), anchor="w")  # Centralize verticalmente com pady (10, 10), adicione padx esquerda (10)

entry_origem = ttk.Entry(frame, font=fonte_origem)
entry_origem.pack(pady=5, anchor="w")  # Adicione anchor="w"

# Botão para selecionar o diretório de origem
fonte_botao = ("Verdana", 12, "bold")  # Escolha a fonte desejada
button_selecionar_origem = ttk.Button(frame, text="Selecionar Origem", command=selecionar_diretorio_origem, style="TButton")
button_selecionar_origem.configure(style="Custom.TButton")  # Configure o estilo personalizado

# Defina a cor de fundo do botão para #014C69
style.configure("Custom.TButton", background="#014C69", foreground="#014C69")
button_selecionar_origem.pack(pady=(10, 10), padx=(90, 0), anchor="w")



# Campo de entrada para o diretório de destino
fonte_destino = ("Verdana", 14, "bold")  # Escolha a fonte desejada
label_destino = ttk.Label(frame, text="Diretório de Destino:", font=fonte_destino)

# Defina a cor de fundo da etiqueta (label) para #014C69
label_destino.configure(background="#014C69")

# Defina a cor do texto para branco (#FFFFFF)
label_destino.configure(foreground="#FFFFFF")

label_destino.pack(pady=(10, 10), padx=(30, 0), anchor="w")  # Centralize verticalmente com pady (10, 10), adicione padx esquerda (12)

entry_destino = ttk.Entry(frame, font=fonte_destino)
entry_destino.pack(pady=5, anchor="w")  # Adicione anchor="w"



# Crie um novo frame para os botões restantes
frame_botoes_2 = tk.Frame(frame, bg="#014C69")
frame_botoes_2.pack(padx=10, pady=10, anchor="w")

# Botão para selecionar o diretório de destino
button_selecionar_destino = ttk.Button(frame_botoes_2, text="Selecionar Destino", command=selecionar_diretorio_destino, style="Custom.TButton")
button_selecionar_destino.configure(style="Custom.TButton")  # Configure o estilo personalizado
button_selecionar_destino.pack(pady=(10, 10), padx=(90, 0), anchor="w")

# Botão para copiar a imagem mais recente
button_copiar_imagem = ttk.Button(frame_botoes_2, text="Copiar Imagem", command=lambda: copiar_ultima_imagem(entry_origem.get(), entry_destino.get(), entry_cliente.get()), style="Custom.TButton")
button_copiar_imagem.configure(style="Custom.TButton")  # Configure o estilo personalizado
button_copiar_imagem.pack(pady=(10, 10), padx=(100, 0), anchor="w")

# Botão para abrir a página da web
button_abrir_pagina = ttk.Button(frame_botoes_2, text="Abrir WhatsApp Web e Enviar ao Cliente", command=abrir_pagina_web, style="Custom.TButton")
button_abrir_pagina.configure(style="Custom.TButton")  # Configure o estilo personalizado
button_abrir_pagina.pack(pady=(10, 10), padx=(30, 0), anchor="w")




root.mainloop()

