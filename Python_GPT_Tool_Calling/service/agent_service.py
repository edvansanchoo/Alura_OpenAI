import os
import json
from openai import OpenAI
from service.file_service import *

class AgentBuilderService:
    def __init__(self, modelo="gpt-4o", sourceAgent="OpenAI"):
        if sourceAgent == "OpenAI":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif sourceAgent == "GitHubModels":
            self.client = OpenAI(
                api_key=os.getenv("GITHUB_TOKEN"),
                base_url="https://models.inference.ai.azure.com"
            )

        self.modelo = modelo
        self.sourceAgent = sourceAgent
        self.tools = self._definir_ferramentas()

    def _definir_ferramentas(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "listar_arquivos",
                    "description": "Lista todos os arquivos em um diretório específico",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "diretorio": {
                                "type": "string",
                                "description": "Caminho do diretório a ser listado"
                            }
                        },
                        "required": ["diretorio"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "ler_arquivo",
                    "description": "Lê o conteúdo de um arquivo",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "caminho_arquivo": {
                                "type": "string",
                                "description": "Caminho do arquivo a ser lido"
                            }
                        },
                        "required": ["caminho_arquivo"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "escrever_arquivo",
                    "description": "Escreve conteúdo em um arquivo",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "caminho_arquivo": {
                                "type": "string",
                                "description": "Caminho do arquivo"
                            },
                            "conteudo": {
                                "type": "string",
                                "description": "Conteúdo a ser escrito"
                            }
                        },
                        "required": ["caminho_arquivo", "conteudo"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "apagar_arquivo",
                    "description": "Apaga um arquivo",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "caminho_arquivo": {
                                "type": "string",
                                "description": "Caminho do arquivo a ser apagado"
                            }
                        },
                        "required": ["caminho_arquivo"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "criar_diretorio",
                    "description": "Cria um novo diretório",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "caminho_diretorio": {
                                "type": "string",
                                "description": "Caminho do diretório a ser criado"
                            }
                        },
                        "required": ["caminho_diretorio"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "apagar_diretorio",
                    "description": "Apaga um diretório",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "caminho_diretorio": {
                                "type": "string",
                                "description": "Caminho do diretório a ser apagado"
                            }
                        },
                        "required": ["caminho_diretorio"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "mover_arquivo",
                    "description": "Move um arquivo de um local para outro",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "caminho_origem": {
                                "type": "string",
                                "description": "Caminho do arquivo de origem"
                            },
                            "caminho_destino": {
                                "type": "string",
                                "description": "Caminho do arquivo de destino"
                            }
                        },
                        "required": ["caminho_origem", "caminho_destino"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "listar_diretorios",
                    "description": "Lista todos os diretórios em um diretório específico",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "diretorio": {
                                "type": "string",
                                "description": "Caminho do diretório a ser listado"
                            }
                        },
                        "required": ["diretorio"]
                    }
                }
            }
        ]

    def _executar_ferramenta(self, nome_funcao, argumentos):
        """Executa a ferramenta chamada pelo agente"""
        
        # Mapa de funções que retornam JSON
        funcoes_json = {
            "listar_arquivos": lambda args: json.dumps(listar_arquivos(args["diretorio"])),
            "listar_diretorios": lambda args: json.dumps(listar_diretorios(args["diretorio"])),
        }
        
        # Mapa de funções que retornam mensagem de sucesso
        funcoes_acao = {
            "ler_arquivo": lambda args: ler_arquivo(args["caminho_arquivo"]),
            "escrever_arquivo": lambda args: (escrever_arquivo(args["caminho_arquivo"], args["conteudo"]), "Arquivo escrito com sucesso")[1],
            "apagar_arquivo": lambda args: (apagar_arquivo(args["caminho_arquivo"]), "Arquivo apagado com sucesso")[1],
            "criar_diretorio": lambda args: (criar_diretorio(args["caminho_diretorio"]), "Diretório criado com sucesso")[1],
            "apagar_diretorio": lambda args: (apagar_diretorio(args["caminho_diretorio"]), "Diretório apagado com sucesso")[1],
            "mover_arquivo": lambda args: (mover_arquivo(args["caminho_origem"], args["caminho_destino"]), "Arquivo movido com sucesso")[1],
        }
        
        # Combinar todos os mapas
        todas_funcoes = {**funcoes_json, **funcoes_acao}
        
        # Executar ou retornar erro
        if nome_funcao in todas_funcoes:
            return todas_funcoes[nome_funcao](argumentos)
    
        return "Ferramenta não encontrada"

    def responder_com_historico(self, historico, prompt, roles):
        mensagens = [
            {"role": "system", "content": roles},
            *historico,
            {"role": "user", "content": prompt}
        ]

        # Loop para processar tool calls
        while True:
            if self.sourceAgent == "OpenAI":
                response = self.client.responses.create(
                    model=self.modelo,
                    input=mensagens,
                    tools=self.tools
                )
                texto = response.output_text
            else:
                response = self.client.chat.completions.create(
                    model=self.modelo,
                    messages=mensagens,
                    tools=self.tools
                )
                
                # Verificar se há tool calls
                if response.choices[0].message.tool_calls:
                    tool_calls = response.choices[0].message.tool_calls
                    
                    # Adicionar resposta do assistente
                    mensagens.append({"role": "assistant", "content": response.choices[0].message.content or "", "tool_calls": tool_calls})
                    
                    # Executar cada ferramenta
                    for tool_call in tool_calls:
                        resultado = self._executar_ferramenta(
                            tool_call.function.name,
                            json.loads(tool_call.function.arguments)
                        )
                        
                        mensagens.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_call.function.name,
                            "content": resultado
                        })
                    
                    continue  # Voltar ao loop para processar a resposta final
                
                texto = response.choices[0].message.content

            break

        historico.append({"role": "user", "content": prompt})
        historico.append({"role": "assistant", "content": texto})

        return texto