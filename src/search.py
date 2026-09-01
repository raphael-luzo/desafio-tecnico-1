from __future__ import annotations

from typing import Any

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres import PGVector

try:
    from config import load_settings
except ModuleNotFoundError:
    from src.config import load_settings

FALLBACK_RESPONSE = "Não tenho informações necessárias para responder sua pergunta."

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def _build_vector_store() -> PGVector:
    settings = load_settings()
    embeddings = OpenAIEmbeddings(
        model=settings.openai_embedding_model,
        api_key=settings.openai_api_key,
    )
    return PGVector(
        embeddings=embeddings,
        collection_name=settings.pg_vector_collection_name,
        connection=settings.database_url,
        use_jsonb=True,
    )


def _normalize_response(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        text_parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(str(item.get("text", "")))
        return "\n".join(text_parts).strip()
    return str(content).strip()


def answer_question(question: str) -> str:
    normalized_question = question.strip()
    if not normalized_question:
        return FALLBACK_RESPONSE

    settings = load_settings()
    vector_store = _build_vector_store()
    results = vector_store.similarity_search_with_score(normalized_question, k=10)
    context = "\n\n".join(
        document.page_content.strip()
        for document, _score in results
        if document.page_content and document.page_content.strip()
    ).strip()
    if not context:
        return FALLBACK_RESPONSE

    prompt = PROMPT_TEMPLATE.format(contexto=context, pergunta=normalized_question)
    llm = ChatOpenAI(
        model=settings.openai_chat_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )
    response = llm.invoke(prompt)
    answer = _normalize_response(response.content)
    return answer or FALLBACK_RESPONSE
