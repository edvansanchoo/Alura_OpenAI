import base64
import cv2
import numpy as np
import os

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