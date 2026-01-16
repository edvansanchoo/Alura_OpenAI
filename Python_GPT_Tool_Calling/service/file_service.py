import os

def listar_arquivos(diretorio):
    """Lista todos os arquivos em um diretório especificado.

    Args:
        diretorio (str): O caminho do diretório a ser listado.

    Returns:
        list: Uma lista de nomes de arquivos no diretório.
    """

    try:
        arquivos = os.listdir(diretorio)
        return [arquivo for arquivo in arquivos if os.path.isfile(os.path.join(diretorio, arquivo))]
    except FileNotFoundError:
        print(f"O diretório {diretorio} não foi encontrado.")
        return []
    except Exception as e:
        print(f"Ocorreu um erro ao listar os arquivos: {e}")
        return []
    
def ler_arquivo(caminho_arquivo):
    """Lê o conteúdo de um arquivo especificado.

    Args:
        caminho_arquivo (str): O caminho do arquivo a ser lido.

    Returns:
        str: O conteúdo do arquivo.
    """

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
        return conteudo
    except FileNotFoundError:
        print(f"O arquivo {caminho_arquivo} não foi encontrado.")
        return ""
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return ""

def escrever_arquivo(caminho_arquivo, conteudo):
    """Escreve conteúdo em um arquivo especificado.

    Args:
        caminho_arquivo (str): O caminho do arquivo onde o conteúdo será escrito.
        conteudo (str): O conteúdo a ser escrito no arquivo.
    """

    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo)
        print(f"Conteúdo escrito com sucesso em {caminho_arquivo}.")
    except Exception as e:
        print(f"Ocorreu um erro ao escrever no arquivo: {e}")

def apagar_arquivo(caminho_arquivo):
    """Apaga um arquivo especificado.

    Args:
        caminho_arquivo (str): O caminho do arquivo a ser apagado.
    """

    try:
        os.remove(caminho_arquivo)
        print(f"O arquivo {caminho_arquivo} foi apagado com sucesso.")
    except FileNotFoundError:
        print(f"O arquivo {caminho_arquivo} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao apagar o arquivo: {e}")

def listar_diretorios(diretorio):
    """Lista todos os diretórios em um diretório especificado.

    Args:
        diretorio (str): O caminho do diretório a ser listado.

    Returns:
        list: Uma lista de nomes de diretórios no diretório.
    """

    try:
        itens = os.listdir(diretorio)
        return [item for item in itens if os.path.isdir(os.path.join(diretorio, item))]
    except FileNotFoundError:
        print(f"O diretório {diretorio} não foi encontrado.")
        return []
    except Exception as e:
        print(f"Ocorreu um erro ao listar os diretórios: {e}")
        return []

def criar_diretorio(caminho_diretorio):
    """Cria um diretório especificado.

    Args:
        caminho_diretorio (str): O caminho do diretório a ser criado.
    """

    try:
        os.makedirs(caminho_diretorio, exist_ok=True)
        print(f"O diretório {caminho_diretorio} foi criado com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao criar o diretório: {e}")

def apagar_diretorio(caminho_diretorio):
    """Apaga um diretório especificado.

    Args:
        caminho_diretorio (str): O caminho do diretório a ser apagado.
    """

    try:
        os.rmdir(caminho_diretorio)
        print(f"O diretório {caminho_diretorio} foi apagado com sucesso.")
    except FileNotFoundError:
        print(f"O diretório {caminho_diretorio} não foi encontrado.")
    except OSError:
        print(f"O diretório {caminho_diretorio} não está vazio ou não pode ser apagado.")
    except Exception as e:
        print(f"Ocorreu um erro ao apagar o diretório: {e}")

def mover_arquivo(caminho_origem, caminho_destino):
    """Move um arquivo de um local para outro.

    Args:
        caminho_origem (str): O caminho do arquivo de origem.
        caminho_destino (str): O caminho do arquivo de destino.
    """

    try:
        os.rename(caminho_origem, caminho_destino)
        print(f"O arquivo foi movido de {caminho_origem} para {caminho_destino} com sucesso.")
    except FileNotFoundError:
        print(f"O arquivo {caminho_origem} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao mover o arquivo: {e}")
