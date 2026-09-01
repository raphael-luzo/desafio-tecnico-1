# Desafio Técnico — Ingestão e Busca Semântica com LangChain + PostgreSQL/pgVector

Este projeto realiza:

1. **Ingestão** de um PDF em chunks com embeddings salvos no PostgreSQL com pgVector.
2. **Busca semântica** via CLI, respondendo apenas com base no conteúdo do PDF.

## Requisitos

- Python 3.11+
- Docker e Docker Compose
- Chave da OpenAI

## Estrutura

```text
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── src/
│   ├── config.py
│   ├── ingest.py
│   ├── search.py
│   └── chat.py
├── document.pdf
└── README.md
```

## Configuração

1. Crie e ative o ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie o arquivo `.env`:

```bash
cp .env.example .env
```

4. Preencha `OPENAI_API_KEY` no `.env`.
5. Se a porta `5432` já estiver em uso na sua máquina, altere `POSTGRES_PORT` e ajuste `DATABASE_URL` para a mesma porta.

## Ordem de execução

1. Subir banco:

```bash
docker compose up -d
```

2. Executar ingestão do PDF:

```bash
python src/ingest.py
```

3. Rodar o chat:

```bash
python src/chat.py
```

## Exemplo de uso

```text
Faça sua pergunta:
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.
```

Pergunta fora de contexto:

```text
PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

## Observações

- Split configurado com `chunk_size=1000` e `chunk_overlap=150`.
- A busca usa `similarity_search_with_score(query, k=10)`.
- A resposta fora de contexto deve ser:
  `Não tenho informações necessárias para responder sua pergunta.`
