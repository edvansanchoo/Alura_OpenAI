from openai import OpenAI
from selecionar_persona import *
from helpers import *
import os

class AssistenteEcoMart:
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

    def responder_com_historico(self, historico, prompt, roles):

        mensagens = [
            {"role": "system", "content": roles},
            *historico,
            {"role": "user", "content": prompt}
        ]

        # 🔹 OpenAI (API nova)
        if self.sourceAgent == "OpenAI":
            response = self.client.responses.create(
                model=self.modelo,
                input=mensagens
            )
            texto = response.output_text

        # 🔹 GitHub Models (Chat Completions)
        else:
            response = self.client.chat.completions.create(
                model=self.modelo,
                messages=mensagens
            )
            texto = response.choices[0].message.content

        historico.append({"role": "user", "content": prompt})
        historico.append({"role": "assistant", "content": texto})

        return texto


    def analisar_imagem(self, caminho_imagem, roles):
        imagem_base64 = encodar_imagem(caminho_imagem)

        resposta = self.client.chat.completions.create(
            model=self.modelo,
            messages=[
                {
                "role": "user",
                "content": [
                    {
                        "type": "text", "text": roles
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{imagem_base64}",
                        },
                    },
                ],
                }
            ],
            max_tokens=300,
            )
        return resposta.choices[0].message.content