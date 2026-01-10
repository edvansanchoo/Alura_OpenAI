from flask import Flask,render_template, request, Response, session
from dotenv import load_dotenv
from helpers import *
from selecionar_persona import *
from assistente_ecomart import *
import os


load_dotenv()

contexto = carrega("dados/ecomart.txt")

assistente = AssistenteEcoMart(
    contexto=contexto,
    persona=personas["neutro"],
    sourceAgent="GitHubModels"
)



app = Flask(__name__)
app.secret_key = 'alura'

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]

    if "historico" not in session:
        session["historico"] = []

    try:
        resposta = assistente.responder(session["historico"], prompt)
        session.modified = True
        try:
            return resposta.content[0].text.value
        except Exception:
            return resposta
    except Exception as erro:
        return Response(f"Erro no GPT: {erro}", status=500)


@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
