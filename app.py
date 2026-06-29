from flask import Flask
from database import conectar

app = Flask(__name__)

app.secret_key = "123"


@app.route("/")
def inicio():

    conexao = conectar()

    return "Sistema HelpDesk funcionando!"


if __name__ == "__main__":
    app.run(debug=True)