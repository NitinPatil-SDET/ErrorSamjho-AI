from connection import create_groq_client


def main():
    try:
        client = create_groq_client()
        models = client.models.list()

        print("\nAvailable Groq models:\n")

        for model in sorted(models.data, key=lambda item: item.id):
            print(model.id)

    except Exception as error:
        print(f"Unable to retrieve models: {error}")


if __name__ == "__main__":
    main()