from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str
    openai_api_key: str
    openai_embedding_model: str
    openai_chat_model: str
    pg_vector_collection_name: str
    pdf_path: str


def _required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"A variável de ambiente {name} é obrigatória.")
    return value


def _optional_env(name: str, default: str) -> str:
    value = os.getenv(name, "").strip()
    return value or default


def load_settings() -> Settings:
    return Settings(
        database_url=_required_env("DATABASE_URL"),
        openai_api_key=_required_env("OPENAI_API_KEY"),
        openai_embedding_model=_optional_env(
            "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
        ),
        openai_chat_model=_optional_env("OPENAI_CHAT_MODEL", "gpt-5-nano"),
        pg_vector_collection_name=_optional_env(
            "PG_VECTOR_COLLECTION_NAME", "document_chunks"
        ),
        pdf_path=_optional_env("PDF_PATH", "document.pdf"),
    )
