from flask import Flask,render_template, request, Response, session
from dotenv import load_dotenv
from helpers import *
from selecionar_persona import *
from assistente_ecomart import *
import os


load_dotenv()

contexto = carrega("dados/ecomart.txt")
UPLOAD_FOLDER = "dados/imagens"
global CAMINHO_IMAGEM_ENVIADA
CAMINHO_IMAGEM_ENVIADA = ""

assistente = AssistenteEcoMart(
    sourceAgent="GitHubModels"
)

roles_Analise_Imagem = """"
        Assuma que você é um assistente de chatbot e que provaelmente o usuário está enviado a foto de
        um produto. Faça uma análise dele, e se for um produto com defeito, emita um parecer. Assuma que você sabe e
        processou uma imagem com o Vision e a resposta será informada no formato de saída.

        # FORMATO DA RESPOSTA
       
         Minha análise para imagem consiste em: Parecer com indicações do defeito ou descrição do produto (se não houver defeito)

        ## Descreva a imagem
        coloque a descrição aqui
    """


app = Flask(__name__)
app.secret_key = 'alura'

@app.route('/upload_imagem', methods=['POST'])
def upload_imagem():
    if 'imagem' in request.files:
        imagem_enviada = request.files['imagem']
        global CAMINHO_IMAGEM_ENVIADA
        CAMINHO_IMAGEM_ENVIADA = salvar_imagem(UPLOAD_FOLDER, imagem_enviada)
    return 'Nenhum arquivo foi enviado', 400






@app.route("/chat", methods=["POST"])
def chat():
    global CAMINHO_IMAGEM_ENVIADA

    prompt = request.json["msg"]

    if "historico" not in session:
        session["historico"] = []

    try:
        
        persona = personas[selecionar_persona(assistente, prompt)]
        analise_imagem = ""
        
        if CAMINHO_IMAGEM_ENVIADA:
            analise_imagem = assistente.analisar_imagem(CAMINHO_IMAGEM_ENVIADA, roles_Analise_Imagem)
            deletar_imagem(CAMINHO_IMAGEM_ENVIADA)
            CAMINHO_IMAGEM_ENVIADA = ""

        if analise_imagem:
            roles = f"""
                #Conteudo da Imagem:

                {analise_imagem}
            """
        else:
            roles = f"""
                Você é um chatbot de atendimento a clientes de um e-commerce.
                Você NÃO deve responder perguntas fora do ecommerce.

                ## Contexto
                {contexto}

                Assuma, de agora em diante, a persona abaixo e ignore as personalidades anteriores.

                ## Persona
                {persona}
                """
        
        resposta = assistente.responder_com_historico(session["historico"], prompt, roles)
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
