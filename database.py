import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def conectar():

    try:

        conexao = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        print("Banco conectado com sucesso!")

        return conexao

    except Exception as erro:

        print("Erro ao conectar:")
        print(repr(erro))


def validar_login(nome, senha):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT *
        FROM usuarios
        WHERE nome=%s
        AND senha=%s
        """,
        (nome, senha)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return usuario


def inserir_chamado(cliente, descricao, prioridade):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO chamados
        (cliente, descricao, prioridade, status, statusfinal)

        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            cliente,
            descricao,
            prioridade,
            "Aberto",
            False
        )
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def listar_chamados():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            cliente,
            descricao,
            prioridade,
            status
        FROM chamados
        WHERE statusfinal = FALSE
        ORDER BY id
        """
    )

    chamados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return chamados


def atualizar_status(id, status):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE chamados
        SET status=%s
        WHERE id=%s
        """,
        (status, id)
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def cancelar_chamado(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE chamados
        SET statusfinal=TRUE
        WHERE id=%s
        """,
        (id,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()