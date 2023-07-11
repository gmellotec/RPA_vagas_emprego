from botcity.web import WebBot, Browser, By
from configparser import ConfigParser

config = ConfigParser()
config.read(r'config\config.ini')


def capturar_links(driver):
    ## ABRIR PAGINA
    site = config.get('links', 'link_serra_news')
    driver.get(site)

    ## 1 - ENTRAR NO LINK PRINCIPAL E PEGAR TODOS OS LINKS DE VAGAS
    lista_links = []
    lista_vagas = driver.find_elements(By.CLASS_NAME, "zox-art-title")

    for vaga in lista_vagas:
        if "emprego" in vaga.text:
            elemento_texto = vaga.find_element(By.TAG_NAME, 'a')
            link = elemento_texto.get_attribute('href')
            lista_links.append(link)
            # print(link)

    print(f'QUANTIDADE DE LINKS ENCONTRADOS: {len(lista_links)}')

    driver.close()
    return lista_links
