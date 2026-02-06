# Python GPT RAG

## 📋 Objetivo do Projeto

Um sistema de **Retrieval-Augmented Generation (RAG)** que responde perguntas baseadas em documentos específicos. O projeto carrega um documento de texto, cria embeddings vetoriais e utiliza um modelo de linguagem para gerar respostas contextualmente relevantes.

## 🎯 O que é RAG?

RAG (Retrieval-Augmented Generation) é uma técnica que combina:
- **Retrieval**: Busca de trechos relevantes em um banco de dados vetorial
- **Augmented**: Enriquecimento do prompt com contexto encontrado
- **Generation**: Geração de resposta por um LLM baseado no contexto

## 🛠️ Tecnologias Utilizadas

- **LangChain**: Framework para construção de aplicações com LLMs
- **Azure OpenAI / GitHub Models**: Modelo de linguagem (GPT-4o-mini)
- **HuggingFace Embeddings**: Embeddings vetoriais locais
- **FAISS**: Banco de dados vetorial para busca rápida
- **Python 3.10+**

## 📁 Estrutura do Projeto

```
.
├── main.py                    # Script principal
├── documentos/
│   └── GTB_gold_Nov23.txt     # Documento de referência
├── service/
│   └── agent_service.py       # (Opcional) Serviços adicionais
└── .env                       # Variáveis de ambiente (não incluir no git)
```

## 📦 Instalação

### 1. Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### 2. Clonar/Configurar o Projeto
```bash
cd Python_GPT_RAG
```

### 3. Criar Ambiente Virtual (Recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 4. Instalar Dependências
```bash
pip install langchain langchain-openai langchain-community langchain-huggingface sentence-transformers faiss-cpu python-dotenv
```

Ou instale todas de uma vez:
```bash
pip install -r requirements.txt
```

### 5. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
GITHUB_TOKEN=seu_token_github_aqui
```

**Nota**: Se estiver usando OpenAI diretamente, adicione:
```env
OPENAI_API_KEY=sua_chave_openai_aqui
```

## 🚀 Como Usar

### Executar o Script Principal
```bash
python main.py
```

### Fazer Perguntas Personalizadas
Edite a última linha do `main.py`:

```python
# Altere a pergunta aqui
print(responder("Sua pergunta sobre o documento"))
```

Exemplos de perguntas:
- "Como devo proceder caso tenha um item roubado?"
- "Quais são os principais benefícios?"
- "Como entrar em contato com suporte?"

## 🔧 Configurações

No arquivo `main.py`, você pode ajustar:

```python
# Modelo e temperatura
modelo = ChatOpenAI(
    temperature=0.5,  # 0 = determinístico, 1 = criativo
    model="gpt-4o-mini"
)

# Tamanho dos chunks e overlap
pedacos = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Tamanho de cada trecho
    chunk_overlap=100     # Sobreposição entre trechos
)

# Número de trechos recuperados
dados_recuperados.as_retriever(search_kwargs={"k": 2})  # Aumentar para mais contexto
```

## 📄 Adicionar Novos Documentos

1. Coloque o arquivo `.txt` em `documentos/`
2. Altere o caminho em `main.py`:

```python
documento = TextLoader(
    "documentos/seu_documento.txt", 
    encoding="utf8"
).load()
```

## ⚠️ Resolvendo Erros Comuns

### Erro 429 - Quota Excedida
- Verifique sua conta OpenAI/GitHub Models
- Certifique-se que tem saldo disponível
- Use embeddings locais (já configurado no projeto)

### Erro: Módulo não encontrado
- Execute `pip install -r requirements.txt` novamente
- Ative o ambiente virtual correto

### Erro: Arquivo não encontrado
- Verifique o caminho do documento em `documentos/`
- Use caminhos relativos a partir da raiz do projeto

## 📝 Notas

- Os embeddings são criados localmente usando HuggingFace (sem custos)
- Apenas as chamadas ao modelo GPT consomem quota
- Os embeddings são recriados a cada execução (considere armazená-los para otimizar)

## 🔐 Segurança

- **Nunca** commit o arquivo `.env` com credenciais no GitHub
- Use um `.gitignore`:

```
.env
venv/
__pycache__/
*.pyc
```

## 📚 Referências

- [LangChain Documentation](https://python.langchain.com/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [HuggingFace Transformers](https://huggingface.co/transformers/)
