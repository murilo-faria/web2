import os
from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv

from database import (
    validar_login,
    inserir_chamado,
    listar_chamados,
    atualizar_status,
    cancelar_chamado
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def home():

    if "usuario" not in session:
        return redirect("/login")

    return render_template(
        "index.html",
        usuario=session["usuario"]
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        senha = request.form["senha"]

        resultado = validar_login(usuario, senha)

        if resultado:

            session["usuario"] = usuario
            return redirect("/")

        return render_template(
            "login.html",
            erro="Usuário ou senha inválidos."
        )

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@app.route("/novo", methods=["GET", "POST"])
def novo():

    if "usuario" not in session:
        return redirect("/login")

    if request.method == "POST":

        cliente = request.form["cliente"]
        descricao = request.form["descricao"]
        prioridade = request.form["prioridade"]

        inserir_chamado(
            cliente,
            descricao,
            prioridade
        )

        return redirect("/fila")

    return render_template("novo_chamado.html")


@app.route("/fila")
def fila():

    if "usuario" not in session:
        return redirect("/login")

    chamados = listar_chamados()

    return render_template(
        "chamados.html",
        chamados=chamados
    )


@app.route("/atender/<int:id>")
def atender(id):

    if "usuario" not in session:
        return redirect("/login")

    atualizar_status(id, "Em Atendimento")

    return redirect("/fila")


@app.route("/concluir/<int:id>")
def concluir(id):

    if "usuario" not in session:
        return redirect("/login")

    atualizar_status(id, "Resolvido")

    return redirect("/fila")


@app.route("/cancelar/<int:id>")
def cancelar(id):

    if "usuario" not in session:
        return redirect("/login")

    cancelar_chamado(id)

    return redirect("/fila")


if __name__ == "__main__":
    app.run(debug=True)