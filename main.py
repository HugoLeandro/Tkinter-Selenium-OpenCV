import cv2
import os
import tkinter as tk
from tkinter import filedialog, ttk
import datetime
from PIL import Image, ImageTk
from selenium import webdriver  # Importar o módulo webdriver do Selenium
from selenium.webdriver.common.keys import Keys
import time

# Variável global para o driver do Selenium
driver = None

# Função para abrir a página da web usando o Selenium
def abrir_pagina_web():
    global driver
    if driver is None:
        driver = webdriver.Chrome()
    driver.get("https://web.whatsapp.com")  # Abre a página do WhatsApp Web

    while True:
        try:
            # Localize o campo de pesquisa no WhatsApp Web
            campo_pesquisa = driver.find_element_by_xpath('//div[@contenteditable="true"][@data-tab="3"]')

            # Verifique se o campo de pesquisa está visível, o que indica que o login foi concluído
            if campo_pesquisa.is_displayed():
                print("Login concluído.")
                break
            else:
                time.sleep(2)  # Aguarde por 2 segundos antes de verificar novamente
        except Exception as e:
            print(f"Erro ao verificar o login: {e}")
            break

    # Obtenha o nome do cliente do campo de entrada do Tkinter
    nome_cliente = entry_cliente.get()

    # Preencha o campo de pesquisa com o nome do cliente
    campo_pesquisa.send_keys(nome_cliente)

    # Pressione a tecla "Enter" para iniciar a pesquisa
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
    imagem_de_fundo = Image.open("colorful_galaxy.jpg")  # Substitua pelo seu caminho de imagem
    imagem_de_fundo = imagem_de_fundo.resize((largura_janela, altura_janela), Image.ANTIALIAS)
    foto_de_fundo = ImageTk.PhotoImage(imagem_de_fundo)
    label_fundo = tk.Label(root, image=None)
    label_fundo.config(image=foto_de_fundo)
    label_fundo.image = foto_de_fundo



def cortar_e_salvar_ultimas_dois(diretorio_origem, diretorio_destino, nome_cliente):
    # Listar todos os arquivos no diretório de origem
    arquivos = os.listdir(diretorio_origem)

    # Filtrar apenas arquivos de imagem (por extensão)
    extensoes_validas = [".jpg", ".jpeg", ".png"]
    arquivos_imagem = [arquivo for arquivo in arquivos if os.path.splitext(arquivo)[1].lower() in extensoes_validas]

    # Encontrar as imagens mais recentes com base nas datas de modificação
    imagens_recentes = []
    for arquivo in arquivos_imagem:
        caminho_completo = os.path.join(diretorio_origem, arquivo)
        data_modificacao = datetime.datetime.fromtimestamp(os.path.getmtime(caminho_completo))
        imagens_recentes.append((caminho_completo, data_modificacao))

    imagens_recentes.sort(key=lambda x: x[1], reverse=True)  # Classificar pela data, da mais recente para a mais antiga

    # Pegar apenas as duas imagens mais recentes
    imagens_ultimas_dois = imagens_recentes[:2]

    # Definir as coordenadas de corte (y, x, h, w) para a região de interesse
    y, x, h, w = 450, 10, 400, 300

    # Cortar e salvar as imagens mais recentes no diretório de destino
    for i, (caminho_imagem, _) in enumerate(imagens_ultimas_dois):
        img = cv2.imread(caminho_imagem)
        crop = img[y:y+h, x:x+w]

        nome_arquivo_destino = f"{nome_cliente}_print_{i+1}.jpg"  # Nome baseado no nome do cliente
        caminho_destino = os.path.join(diretorio_destino, nome_arquivo_destino)

        cv2.imwrite(caminho_destino, crop)

        print(f"Imagem {i+1} cortada e salva em: {caminho_destino}")




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
imagem_de_fundo = Image.open("colorful_galaxy.jpg")  # Substitua "background.jpg" pelo seu caminho de imagem
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




# Botão para iniciar o processo de corte e salvamento
button_cortar = ttk.Button(root, text="Cortar e Salvar", command=lambda: cortar_e_salvar_ultimas_dois(entry_origem.get(), entry_destino.get(), entry_cliente.get()))
button_cortar.pack(pady=5)  # Adicione mais padding vertical (10 pixels) ao botão

# Botão para iniciar o processo de corte e salvamento
button_cortar = ttk.Button(root, text="Cortar e Salvar", command=lambda: cortar_e_salvar_ultimas_dois(entry_origem.get(), entry_destino.get()))


# Botão para abrir a página da web
button_abrir_pagina = ttk.Button(root, text="Abrir WhatsApp Web e Enviar ao Cliente", command=abrir_pagina_web)
button_abrir_pagina.pack(pady=5)


root.mainloop()
