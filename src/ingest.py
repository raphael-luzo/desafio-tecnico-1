from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

try:
    from config import load_settings
except ModuleNotFoundError:
    from src.config import load_settings


def ingest_pdf() -> None:
    settings = load_settings()
    pdf_path = Path(settings.pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")

    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(
        model=settings.openai_embedding_model,
        api_key=settings.openai_api_key,
    )
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=settings.pg_vector_collection_name,
        connection=settings.database_url,
        use_jsonb=True,
    )
    vector_store.add_documents(chunks)

    print(
        f"Ingestão concluída com sucesso. Páginas: {len(documents)} | "
        f"Chunks: {len(chunks)} | Coleção: {settings.pg_vector_collection_name}"
    )


if __name__ == "__main__":
    try:
        ingest_pdf()
    except (FileNotFoundError, ValueError) as error:
        print(f"Erro na ingestão: {error}")
        raise SystemExit(1)
