try:
    from search import answer_question
except ModuleNotFoundError:
    from src.search import answer_question


def main() -> None:
    print("Faça sua pergunta:")
    while True:
        try:
            question = input("PERGUNTA: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if question.lower() in {"sair", "exit", "quit"}:
            break
        if not question:
            continue

        try:
            answer = answer_question(question)
        except ValueError as error:
            print(f"RESPOSTA: Erro de configuração: {error}")
            break
        print(f"RESPOSTA: {answer}")


if __name__ == "__main__":
    main()
