import Scrap_Solsete_back_end
from tkinter import *
from tkinter import ttk
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, threading
import random
from PIL import ImageTk, Image


def inicializador_pesquisa(caixa_texto_busca, opcao_seletor, opcao_seletor_visual, opcao_seletor_guia, progress_bar, botao_confirmar):
    produto = caixa_texto_busca.get()
    if produto != "" and produto != "Insira um produto":
        log = open("log.txt", "w")
        log.write("iniciando pesquisa" + "\n")
        log.write(produto + "\n")
        log.close()
        tabela = pd.DataFrame(columns=["Site", "Localização", "Data", "Nome do Produto", "Preço"])
        contador = 0

        firefox_options = webdriver.ChromeOptions()
        if "anônima" in opcao_seletor_guia.get():
            firefox_options.add_argument('--incognito')
        if "Oculta" in opcao_seletor_visual.get():
            firefox_options.add_argument("--headless")
        firefox_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser = webdriver.Chrome(options=firefox_options)
        browser.delete_all_cookies()
        browser.set_page_load_timeout(30)

        if  "internacional" in opcao_seletor.get():
            contador = Scrap_Solsete_back_end.coleta_internacional(produto, tabela, contador, browser)
        elif "nacional" in opcao_seletor.get():
            contador = Scrap_Solsete_back_end.coleta_nacional(produto, tabela, contador, browser)
        elif "Ambos" in opcao_seletor.get():
            contador = Scrap_Solsete_back_end.coleta_nacional(produto, tabela, contador, browser)
            contador = Scrap_Solsete_back_end.coleta_internacional(produto, tabela, contador, browser)
        else:
            log = open("log.txt", "a")
            log.write("erro, opcao invalida"+ "\n")
            log.close()
        browser.close()
        Scrap_Solsete_back_end.avaliacao_inicial(produto, tabela, contador)
        tabela.to_excel("Dados_Para_Avaliacao_" + produto.replace(" ", "_") + ".xlsx")
        progress_bar.stop()
        botao_confirmar.config(state="normal")
    else:
        progress_bar.stop()
        botao_confirmar.config(state="normal")
        caixa_texto_busca.delete(0, END)
        caixa_texto_busca.insert(0,"Insira um produto")


def loading(win, botao_confirmar, caixa_texto_busca, opcao_seletor, opcao_seletor_visual, opcao_seletor_guia):
    progress_bar = ttk.Progressbar(win, orient=HORIZONTAL, mode='indeterminate', length=280)
    progress_bar.pack(pady=20)
    botao_confirmar.config(state="disable")
    progress_bar.start()
    threading.Thread(target=inicializador_pesquisa, args=(caixa_texto_busca, opcao_seletor, opcao_seletor_visual, opcao_seletor_guia, progress_bar, botao_confirmar)).start()

def __initapp__(master=None):
    widget = Frame(master)
    widget.pack()

    image_frame = Frame(widget, width=300, height=300)
    image_frame.pack()

    img = ImageTk.PhotoImage(Image.open("logo.jpeg"))
    logo = Label(image_frame, image=img)  
    logo.image = img
    logo.pack()


    titulo = Label(widget, text="Avaliação de Produtos Usados")
    titulo.pack()

    caixa_texto_busca = Entry(widget)

    opcao_seletor = StringVar()
    opcao_seletor.set("Produto nacional")
    seletor_nacional_inter = OptionMenu(widget, opcao_seletor, *["Produto nacional", "Produto Internacional, Ambos"] )

    opcao_seletor_visual = StringVar()
    opcao_seletor_visual.set("Página Oculta")
    seletor_visual = OptionMenu(widget, opcao_seletor_visual, *["Página Visivel", "Página Oculta"] )

    opcao_seletor_guia = StringVar()
    opcao_seletor_guia.set("Navegação anônima")
    seletor_guia = OptionMenu(widget, opcao_seletor_guia, *["Navegação normal", "Navegação anônima"] )

    botao_confirmar = Button(widget, text="Pesquisar", command=lambda : [loading(master, botao_confirmar,caixa_texto_busca, opcao_seletor, opcao_seletor_visual, opcao_seletor_guia)])

    caixa_texto_busca.pack()
    seletor_nacional_inter.pack()
    seletor_visual.pack()
    seletor_guia.pack()
    botao_confirmar.pack()

if __name__ == "__main__":
    root = Tk()
    root.geometry("300x360")
    root.winfo_toplevel().title("Avaliador Solsete")
    root.resizable(False, False)
    __initapp__(root)
    root.mainloop()