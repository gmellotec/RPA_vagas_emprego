import pyodbc
from configparser import ConfigParser

config = ConfigParser()
config.read(r'config\config.ini')


def connect_database():
    try:
        dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                         "Server=localhost;"
                         r"Database=database\vagas_db.db;")
        conexao = pyodbc.connect(dados_conexao)
        print('CONEXAO REALIZADA COM SUCESSO')
        return conexao
    except Exception as erro:
        print(f'Falha na conexao com o banco de dados: {erro} ')


def select_database(conexao, data_post, titulo, link):

    data_post = data_post
    titulo = titulo
    link = link

    cursor = conexao.cursor()

    var_query = """SELECT COUNT(*) 
                           FROM rpa_vagas 
                           WHERE data_post = ? AND nm_vaga = ? AND link = ?"""

    # cursor.execute(var_query, (item['data_post'], item['titulo'], item['link']))
    cursor.execute(var_query, (data_post, titulo, link))

    var_count = cursor.fetchone()[0]

    cursor.close()

    if var_count > 0:
        vaga_existe = True
        return vaga_existe
    else:
        vaga_existe = False
        return vaga_existe


def insert_database(conexao, data_post, titulo, link):

    cursor = conexao.cursor()

    var_query = "INSERT INTO rpa_vagas (data_post, nm_vaga, link) VALUES (?, ?, ?)"

    cursor.execute(var_query, (data_post, titulo, link))

    conexao.commit()

    cursor.close()
