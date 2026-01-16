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
        if nome_funcao == "listar_arquivos":
            return json.dumps(listar_arquivos(argumentos["diretorio"]))
        elif nome_funcao == "ler_arquivo":
            return ler_arquivo(argumentos["caminho_arquivo"])
        elif nome_funcao == "escrever_arquivo":
            escrever_arquivo(argumentos["caminho_arquivo"], argumentos["conteudo"])
            return "Arquivo escrito com sucesso"
        elif nome_funcao == "apagar_arquivo":
            apagar_arquivo(argumentos["caminho_arquivo"])
            return "Arquivo apagado com sucesso"
        elif nome_funcao == "criar_diretorio":
            criar_diretorio(argumentos["caminho_diretorio"])
            return "Diretório criado com sucesso"
        elif nome_funcao == "apagar_diretorio":
            apagar_diretorio(argumentos["caminho_diretorio"])
            return "Diretório apagado com sucesso"
        elif nome_funcao == "mover_arquivo":
            mover_arquivo(argumentos["caminho_origem"], argumentos["caminho_destino"])
            return "Arquivo movido com sucesso"
        elif nome_funcao == "listar_diretorios":
            return json.dumps(listar_diretorios(argumentos["diretorio"]))
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