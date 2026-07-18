from app.bootstrap import create_pipeline


def main():

    print("=" * 80)
    print("GitHub Code Intelligence Assistant")
    print("=" * 80)
    print("Type 'exit' or 'quit' to stop.")
    print()

    print("Loading pipeline...")
    pipeline = create_pipeline()
    print("Pipeline loaded.\n")

    while True:

        try:

            question = input("You > ").strip()

            if not question:
                continue

            if question.lower() in {
                "exit",
                "quit",
                "q",
            }:
                print("\nGoodbye!")
                break

            response = pipeline.ask(question)

            print("\nAssistant")
            print("-" * 80)
            print(response.answer)

            print("\nSources")
            print("-" * 80)

            for i, result in enumerate(
                response.retrieval_results,
                start=1,
            ):

                print(
                    f"{i}. "
                    f"{result.chunk.file_path} "
                    f"({result.score:.4f})"
                )

            print("\nLatency")
            print("-" * 80)

            print(
                f"Retrieval : "
                f"{response.retrieval_latency_ms:.2f} ms"
            )

            print(
                f"Generation: "
                f"{response.generation_latency_ms:.2f} ms"
            )

            print(
                f"Total     : "
                f"{response.total_latency_ms:.2f} ms"
            )

            print("\n" + "=" * 80 + "\n")

        except KeyboardInterrupt:

            print("\n\nGoodbye!")
            break

        except Exception as e:

            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()