import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random

def coletar_olx(produto, tabela, contador, browser):
    chave = produto.replace(" ", "%20")

    browser.get("https://www.olx.com.br/brasil?q="+chave)
    time.sleep(random.randint(4,7))

    paginacao = browser.find_elements_by_css_selector(".sc-1bofr6e-0.hUHECR.sc-gzVnrw.gEAEAL")
    anuncios =  browser.find_elements_by_class_name("huFwya")
    contador_paginas = 0
    x = 0
    if len(anuncios) > 0:
        while contador_paginas <= 10:
            anuncios =  browser.find_elements_by_class_name("huFwya")
            for anuncio in anuncios:
                nome = "Não Indicado"
                preço = "Não Indicado"
                localidade = "Não Indicado"
                data = "Não Indicado"
                tmp_nome = []
                tmp_data = []
                tmp_preco = []
                tmp_local = []

                tmp_nome = anuncio.find_elements_by_class_name("eFXRHn")
                if len(tmp_nome) > 0:
                    nome = tmp_nome[0].text
                if nome == "":
                    nome = "Não Indicado"
                
                tmp_preco = anuncio.find_elements_by_class_name("dGMPPn")
                if len(tmp_preco) > 0:
                    preço = tmp_preco[0].text.replace(".", "").replace(",", ".").replace(" ", "").replace("R$", "")
                if preço == "":
                    preço = "Não Indicado"

                tmp_local = anuncio.find_elements_by_class_name("lfQETj")
                if len(tmp_local) > 0:
                    localidade = tmp_local[0].text

                tmp_data = anuncio.find_elements_by_class_name("javKJU")
                if len(tmp_data) > 0:
                    data = tmp_data[0].text

                if "Não Indicado" not in nome and "Não Indicado" not in preço:
                    tabela.loc[contador] = ["OLX", localidade, data, nome, preço]
                    contador = contador + 1
            contador_paginas = contador_paginas + 1
            if "Próxima" in paginacao[x].text:
                paginacao[x].click()
                if x == 0:
                    x = 1
                time.sleep(random.randint(2,4))
                paginacao = browser.find_elements_by_css_selector(".sc-1bofr6e-0.hUHECR.sc-gzVnrw.gEAEAL")
            else:
                break

    return contador
###############################################

def coletar_mercado_livre(produto, tabela, contador, browser):
    chave = produto.replace(" ", "-")
    time.sleep(random.randint(6,8))
    browser.get("https://lista.mercadolivre.com.br/" + chave)

    browser.find_element_by_css_selector(".cookie-consent-banner-opt-out__action.cookie-consent-banner-opt-out__action--primary.cookie-consent-banner-opt-out__action--key-accept").click()
    botoes = browser.find_elements_by_class_name("ui-search-link")
    usados = [x for x in botoes if "Usado" in x.text]
 
    if len(usados) > 0:
        usados[0].click()
        time.sleep(random.randint(3,5))
    else:
        log = open("log.txt", "a")
        log.write("não foram encontrados produtos usados no mercado livre"+ "\n")
        log.close()
        return contador

    paginacao = browser.find_elements_by_css_selector(".andes-pagination__link.shops__pagination-link.ui-search-link")
    contador_paginas = 0
    x = 0
    while contador_paginas <= 10:
        anuncios = browser.find_elements_by_class_name("ui-search-layout__item")
        for anuncio in anuncios:
            nome = "Não Indicado"
            preço = "Não Indicado"
            tmp_nome = []
            tmp_preco = []

            tmp_nome = anuncio.find_elements_by_class_name("ui-search-item__title")
            if len(tmp_nome) > 0:
                nome = tmp_nome[0].text

            tmp_preco = anuncio.find_elements_by_class_name("price-tag-amount")
            if len(tmp_preco) > 0:
                preço = tmp_preco[0].text.replace("\n", "").replace(".", "").replace(",", ".").replace(" ", "").replace("R$", "")

            if "Não Indicado" not in nome and "Não Indicado" not in preço:
                tabela.loc[contador] = ["Mercado Livre", "Não Indicado", "Não Indicado", nome, preço]
                contador = contador + 1
        contador_paginas = contador_paginas + 1
        if len(paginacao) > 0 and "Seguinte" in paginacao[len(paginacao)-1].text:
            paginacao[len(paginacao)-1].click()
            if x == 0:
                x = 1
            time.sleep(random.randint(4,6))
            paginacao = browser.find_elements_by_css_selector(".andes-pagination__link.shops__pagination-link.ui-search-link")
        else:
            break
    return contador

def coletar_ebay(produto, tabela, contador, browser):
    chave = produto.replace(" ", "+")

    browser.get("https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw="+chave+"&rt=nc&LH_ItemCondition=3000")  
    time.sleep(random.randint(4,7))


    paginacao = browser.find_elements_by_css_selector(".pagination__next.icon-link")
    while len(paginacao) > 0:
        paginacao = browser.find_elements_by_css_selector(".pagination__next.icon-link")
        pagina = browser.find_element_by_class_name("srp-list")
        lista = pagina.find_elements_by_tag_name("li")
        for elemento in lista:
            if "que correspondem a menos palavras" in elemento.text:
                break

            nome = "Não Indicado"
            preço = "Não Indicado"
            localidade = "Não Indicado"
            tmp_nome = []
            tmp_preco = []
            tmp_local = []

            tmp_nome = elemento.find_elements_by_class_name("s-item__title")
            if len(tmp_nome) > 0:
                nome = tmp_nome[0].text
            
            tmp_preco = elemento.find_elements_by_class_name("s-item__price")
            if len(tmp_nome) > 0:
                preço = tmp_preco[0].text.replace("R$", "").replace(" ", "").replace("BRL", "").replace(".", "").replace(",", ".")
                if "a" in preço:
                    valores = preço.split("a")
                    preço = str((float(valores[0]) + float(valores[1])) // 2)
            
            tmp_local = elemento.find_elements_by_class_name("s-item__itemLocation")
            if len(tmp_nome) > 0:
                localidade = tmp_local[0].text

            if "Não Indicado" not in nome and "Não Indicado" not in preço:
                tabela.loc[contador] = ["EBAY", localidade, "Não Indicado", nome, preço]
                contador = contador + 1
        if len(paginacao) > 0:
            paginacao[0].click()
            time.sleep(random.randint(4,6))

    return contador

def coletar_reverb(produto, tabela, contador, browser):
    chave = produto.replace(" ", "%20")
    
    browser.get("https://reverb.com/marketplace?query="+chave+"&condition=used")
    time.sleep(random.randint(4,7))

    lista = browser.find_elements_by_class_name("grid-card")

    lista = browser.find_elements_by_class_name("tiles--four-wide-max")
    if len(lista) > 0:
        for linha in lista:
            lista_produtos = linha.find_elements_by_class_name("grid-card")
            for elemento in lista_produtos:
                nome = "Não Indicado"
                preço = "Não Indicado"
                localidade = "Não Indicado"
                tmp_nome = []
                tmp_preco = []
                tmp_local = []

                tmp_nome = elemento.find_elements_by_class_name("grid-card__main__text")
                if len(tmp_nome) > 0:
                    nome = tmp_nome[0].text
                
                tmp_preco = elemento.find_elements_by_class_name("grid-card__price")
                if len(tmp_nome) > 0:
                    preço = tmp_preco[0].text.replace("R$", "").replace(" ", "").replace("BRL", "").replace(",", "")
                    #print(preço)
                
                tmp_local = elemento.find_elements_by_class_name("listing-shop-country-nudge")
                if len(tmp_nome) > 0:
                    localidade = tmp_local[0].text

                if "Não Indicado" not in nome and "Não Indicado" not in preço:
                    tabela.loc[contador] = ["REVERB", localidade, "Não Indicado", nome, preço]
                    contador = contador + 1
    else:
        lista = browser.find_elements_by_class_name("sortable-tiles")
        if len(lista) == 0:
            log = open("log.txt", "a")
            log.write("Produto não encontrado em Reverb"+ "\n")
            return contador
        
        paginacao = browser.find_elements_by_css_selector(".pagination__button")
        contador_paginas = 0
        while contador_paginas <= 10:
            lista = browser.find_elements_by_class_name("sortable-tile")
            for elemento in lista:
                nome = "Não Indicado"
                preço = "Não Indicado"
                localidade = "Não Indicado"
                tmp_nome = []
                tmp_preco = []
                tmp_local = []

                tmp_nome = elemento.find_elements_by_class_name("grid-card__main__text")
                if len(tmp_nome) > 0:
                    nome = tmp_nome[0].text
                
                tmp_preco = elemento.find_elements_by_class_name("grid-card__price")
                if len(tmp_nome) > 0:
                    preço = tmp_preco[0].text.replace(" ", "").replace("R$", "").replace(",", "").replace("BRL", "")
                
                tmp_local = elemento.find_elements_by_class_name("listing-shop-country-nudge")
                if len(tmp_nome) > 0:
                    localidade = tmp_local[0].text

                if "Não Indicado" not in nome and "Não Indicado" not in preço:
                    tabela.loc[contador] = ["REVERB", localidade, "Não Indicado", nome, preço]
                    contador = contador + 1
            contador_paginas = contador_paginas + 1
            paginacao = browser.find_elements_by_css_selector(".pagination__button")
            if len(paginacao) > 0 and "Next" in paginacao[len(paginacao)-1].text:
                paginacao[len(paginacao)-1].click()
                time.sleep(random.randint(2,4))
            else:
                break
    return contador

def avaliacao_inicial(produto, tabela, contador):
    if contador > 0:
        arquivo = open("Avaliacao" + produto.replace(" ", "_") + ".txt", "w")
        valores = list(tabela['Preço'])

        for x in range(len(valores)):
            valores[x] = float(valores[x])

        soma = 0
        for x in range(len(valores)):
            soma = soma + valores[x]

        arquivo.write("Avaliação para " + produto + "\n")
        arquivo.write("==============================================\n\n")
        arquivo.write("Número de preços pesquisados: " + str(len(valores)) + "\n")
        media = soma/len(valores)
        arquivo.write("Média de preço de todos os produtos: " + str(round(media,2)) + "\n")

        valores.sort()
        if len(valores)%2 == 0:
            mediana = valores[len(valores)//2] + valores[(len(valores)//2)-1]
            mediana = mediana//2
        else:
            mediana = valores[len(valores)//2]
        arquivo.write("Mediana de todos os preços: " + str(round(mediana,2)) + "\n")
        arquivo.write("Menor preço encontrado: " + str(round(valores[0],2)) + "\n")
        arquivo.write("Maior preço encontrado: "+ str(round(valores[len(valores)-1],2)) + "\n")
        arquivo.write("============================================"  + "\n")

        numero_valores_exclusao = len(valores) * 0.1

        for x in range(int(numero_valores_exclusao)):
            valores.pop(x)
            valores.pop(len(valores)-x-1)
        soma = 0
        for x in valores:
            soma = soma + x

        arquivo.write("Avaliação retirando 10% dos valores mais altos e baixos para " + produto + "\n")
        arquivo.write("==============================================\n\n")
        arquivo.write("Número de preços pesquisados: " + str(len(valores)) + "\n")
        media = soma/len(valores)
        arquivo.write("Média de preço de todos os produtos: " + str(round(media,2)) + "\n")

        valores.sort()
        if len(valores)%2 == 0:
            mediana = valores[len(valores)//2] + valores[(len(valores)//2)-1]
            mediana = mediana//2
        else:
            mediana = valores[len(valores)//2]
        arquivo.write("Mediana de todos os preços: " + str(round(mediana,2)) + "\n")
        arquivo.write("Menor preço encontrado: " + str(round(valores[0],2)) + "\n")
        arquivo.write("Maior preço encontrado: "+ str(round(valores[len(valores)-1],2)) + "\n")
        arquivo.write("============================================"  + "\n")

        arquivo.close()


def coleta_nacional(produto, tabela, contador, browser):
    contador = coletar_olx(produto, tabela, contador, browser)
    contador = coletar_mercado_livre(produto, tabela, contador, browser)
    return contador

def coleta_internacional(produto, tabela, contador, browser):
    contador = coletar_ebay(produto, tabela, contador, browser)
    contador = coletar_reverb(produto, tabela, contador, browser)
    return contador



"""if __name__ == "__main__":
    #Colunas - Site / Localização / Data / Nome do Produto / Preço
    contador = 0
    tabela = pd.DataFrame(columns=["Site", "Localização", "Data", "Nome do Produto", "Preço"])

    firefox_options = webdriver.ChromeOptions()
    firefox_options.add_argument('--incognito')
    firefox_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=firefox_options)
    browser.delete_all_cookies()
    browser.set_page_load_timeout(60)

    produto = input("Digite o Nome do Produto para Avaliação: ")

    contador = coleta_nacional(produto, tabela, contador)
    contador = coleta_internacional(produto, tabela, contador)
    tabela.to_excel("Dados_Para_Avaliacao_" + produto.replace(" ", "_") + ".xlsx")
    browser.close()
    avaliacao_inicial(produto, tabela)"""

