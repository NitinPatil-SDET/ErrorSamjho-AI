import pytest

from ai_service import RateLimiter, explain_error


sample_error = """
2026/08/14 15:45:13 - Get Files From Server.0 - File 'BankSapReconUploadFiles1.zip not found on server.
 
"""


def test_rate_limiter_blocks_extra_requests_within_window():
    limiter = RateLimiter(max_calls=2, window_seconds=60)

    assert limiter.acquire() is True
    assert limiter.acquire() is True

    with pytest.raises(RuntimeError, match="Rate limit"):
        limiter.acquire()


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