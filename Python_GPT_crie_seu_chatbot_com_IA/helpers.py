import base64
import cv2
import numpy as np
import os
import uuid

def carrega(nome_do_arquivo):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        caminho_completo = os.path.join(base_dir, nome_do_arquivo)
        
        with open(caminho_completo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")

def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def encodar_imagem(caminho_imagem):
    with open(caminho_imagem, "rb") as arquivo_imagem:
        return base64.b64encode(arquivo_imagem.read()).decode('utf-8')
    
def salvar_imagem(caminho_salvar, imagem_enviada):
    nome_arquivo = str(uuid.uuid4()) + os.path.splitext(imagem_enviada.filename)[1]
    caminho_arquivo = os.path.join(caminho_salvar, nome_arquivo)
    imagem_enviada.save(caminho_arquivo)
    return caminho_arquivo

def deletar_imagem(caminho_imagem):
    if os.path.exists(caminho_imagem):
        os.remove(caminho_imagem)