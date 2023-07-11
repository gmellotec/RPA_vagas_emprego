import time
from datetime import datetime
from config.config_selenium import *
from configparser import ConfigParser
from pages.capturar_links import *
from database import database

config = ConfigParser()
config.read(r'config\config.ini', encoding='utf-8')

## CONFIG SELENIUM
driver = config_selenium()

## CAPTURAR LINKS QUE CONTEM A PALAVRA EMPREGO DO SITE PRINCIPAL
lista_links = capturar_links(driver)

## VAGA QUE DESEJA OBTER RESULTADOS
lista_cargos = config.get('pesquisar', 'vaga').split(',')
lista_cargos_bloq = config.get('pesquisar', 'bloquear').split(',')

lista_encontrados = []
qnt_encontrados = 0

var_loop = 0
for link in lista_links:
    '''Foi necessario fechar a primeira aba e abrir aba por aba
       em cada loop pois o site solicita verificacao caso abra 
       diversas paginas por vez'''

    ## CONFIG SELENIUM
    driver = config_selenium()

    ## ABRIR LINK
    driver.get(link)

    lista_li = driver.find_elements(By.TAG_NAME, 'li')

    for li in lista_li:
        for cargo in lista_cargos:
            if cargo in li.text.lower():
                vaga = {}
                vaga['titulo'] = li.text
                vaga['link'] = link

                # PEGAR A DATA DA POSTAGEM
                tag_time = driver.find_element(By.TAG_NAME, 'time')
                data_post = tag_time.get_attribute('datetime')
                vaga['data_post'] = data_post

                lista_encontrados.append(vaga)
                qnt_encontrados += 1
    var_loop += 1
    print(f'Verificado link: {var_loop}')
    driver.close()

print(lista_encontrados)
print(f'Quantidade de vagas encontradas: {qnt_encontrados}')

if len(lista_encontrados) > 0:
    print('CONECTANDO COM O BANCO DE DADOS')
    conn = database.connect_database()

    for item in lista_encontrados:
        vaga_existe = database.select_database(conn, item['data_post'], item['titulo'], item['link'])

        if not vaga_existe:
            print('REALIZANDO INSERT NO BANCO DE DADOS')
            database.insert_database(conn, item['data_post'], item['titulo'], item['link'])

        else:
            print('VAGA ENCONTRADA JA CONSTA NO BANCO DE DADOS')

    print('FECHANDO CONEXAO COM BANCO DE DADOS')
    conn.close()
    print('FIM DO PROCESSO')
else:
    print('NENHUMA VAGA ENCONTRADA')
    print('FIM DO PROCESSO')
