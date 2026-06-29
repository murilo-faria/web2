import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

print("HOST =", os.getenv("DB_HOST"))
print("PORT =", os.getenv("DB_PORT"))
print("DATABASE =", os.getenv("DB_NAME"))
print("USER =", os.getenv("DB_USER"))
print("PASSWORD =", os.getenv("DB_PASSWORD"))

def conectar():
    try:
        conexao = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="helpdesk",
            user="postgres",
            password="postgres"
        )

        print("Banco conectado com sucesso!")
        return conexao

    except Exception as erro:
        print("Erro ao conectar:")
        print(repr(erro))