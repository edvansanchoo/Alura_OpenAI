from openai import OpenAI
import os

class AssistenteEcoMart:
    def __init__(self, contexto, persona, modelo="gpt-4o", sourceAgent="OpenAI"):
        if sourceAgent == "OpenAI":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif sourceAgent == "GitHubModels":
            self.client = OpenAI(
                api_key=os.getenv("GITHUB_TOKEN"),
                base_url="https://models.inference.ai.azure.com"
            )

        self.modelo = modelo
        self.sourceAgent = sourceAgent

        self.system_prompt = f"""
        Você é um chatbot de atendimento a clientes de um e-commerce.
        Você NÃO deve responder perguntas fora do ecommerce.

        ## Contexto
        {contexto}

        ## Persona
        {persona}
        """

    def responder(self, historico, prompt):
        mensagens = [
            {"role": "system", "content": self.system_prompt},
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
