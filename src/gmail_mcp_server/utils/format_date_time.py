from datetime import datetime, timezone
from urllib.parse import unquote


def format_to_rfc3339(datetime_str: str) -> str:
    """
    Decodes, parses, and formats a datetime string into RFC 3339 UTC format.
    """
    try:
        # First, perform the URL decoding
        decoded_str = unquote(datetime_str)

        # Now, proceed with the parsing logic on the decoded string
        if decoded_str.upper().endswith("Z"):
            dt_obj = datetime.fromisoformat(decoded_str[:-1])
            dt_utc = dt_obj.replace(tzinfo=timezone.utc)
        else:
            # ... (rest of the parsing logic)
            dt_obj = datetime.fromisoformat(decoded_str)
            if dt_obj.tzinfo is None:
                dt_utc = dt_obj.replace(tzinfo=timezone.utc)
            else:
                dt_utc = dt_obj.astimezone(timezone.utc)

        return dt_utc.isoformat().replace("+00:00", "Z")

    except (ValueError, TypeError) as e:
        raise ValueError(
            f"Invalid datetime format after decoding: '{datetime_str}'. Please use ISO 8601 format."
        ) from e
