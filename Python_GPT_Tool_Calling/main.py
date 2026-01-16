from dotenv import load_dotenv
from service.agent_service import *

load_dotenv()

historico = []
DIRETORIO_RAIZ = 'files'
assistente = AgentBuilderService(
    sourceAgent="GitHubModels"
)


roles = f"""
        Você é um agente especializado em arquivos, você tem a capacidade de analisar textos e extrair informações relevantes.
        É capaz de utilizar ferramentas internas para operar nas solicitações dos usuários.
        Todo comando solicitado deve ser executado no diretório raiz: {DIRETORIO_RAIZ}.
        """


while True:
    #limpar o terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n--- Digite uma das opções para sair: sair, exit, quit ---\n")
    prompt = input("Usuário: ")
    
    if prompt.lower() in ["sair", "exit", "quit"]:
        break

    resposta = assistente.responder_com_historico(historico, prompt, roles)
    print("Assistente:", resposta)
