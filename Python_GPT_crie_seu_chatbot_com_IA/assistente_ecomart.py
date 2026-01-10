from openai import OpenAI
from selecionar_persona import *
import os

class AssistenteEcoMart:
    def __init__(self, modelo="gpt-4.1-mini", sourceAgent="OpenAI"):
        if sourceAgent == "OpenAI":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif sourceAgent == "GitHubModels":
            self.client = OpenAI(
                api_key=os.getenv("GITHUB_TOKEN"),
                base_url="https://models.inference.ai.azure.com"
            )

        self.modelo = modelo
        self.sourceAgent = sourceAgent

    def responder(self, historico, prompt, contexto):
        persona = personas[selecionar_persona(self, prompt)]

        system_prompt = f"""
            Você é um chatbot de atendimento a clientes de um e-commerce.
            Você NÃO deve responder perguntas fora do ecommerce.

            ## Contexto
            {contexto}

            Assuma, de agora em diante, a persona abaixo e ignore as personalidades anteriores.

            ## Persona
            {persona}
            """

        mensagens = [
            {"role": "system", "content": system_prompt},
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
