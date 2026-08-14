from prompt import create_error_prompt


sample_error = ""


try:
    final_prompt = create_error_prompt(sample_error)

    print("Prompt created successfully.")
    print("=" * 70)
    print(final_prompt)

except ValueError as error:
    print(f"Input Error: {error}")

except TypeError as error:
    print(f"Type Error: {error}")

except Exception as error:
    print(f"Unexpected Error: {error}")