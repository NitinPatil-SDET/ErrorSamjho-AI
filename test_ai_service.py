from ai_service import explain_error


sample_error = """
2026/08/14 15:45:13 - Get Files From Server.0 - File 'BankSapReconUploadFiles1.zip not found on server.
 
"""


def main():
    print("Sending error to ErrorSamjho AI...")
    print("Please wait.\n")

    try:
        result = explain_error(sample_error)

        print("=" * 70)
        print("ERRORSAMJHO AI RESPONSE")
        print("=" * 70)
        print(result)
        print("=" * 70)

    except ValueError as error:
        print(f"Input or Response Error: {error}")

    except RuntimeError as error:
        print(f"AI Service Error: {error}")

    except Exception as error:
        print(f"Unexpected Error: {error}")


if __name__ == "__main__":
    main()