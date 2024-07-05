import re
import time


def save_document_to_disk(directory_path: str, title: str, body: str) -> str:
    document_file_name = get_safe_file_name(title)
    document_file_path = f"{directory_path}/{document_file_name}"

    with open(document_file_path, "w") as file:
        # Append data to the file
        file.write(body)

    return document_file_path


def get_safe_file_name(name: str, file_extension: str = ".txt") -> str:
    # Replace characters not allowed in filenames with underscore
    safe_file_name = re.sub(r"[^\w\-_. ]", "_", name)
    safe_file_name = safe_file_name.strip()
    # Replace consecutive spaces with single space
    safe_file_name = re.sub(r"\s+", " ", safe_file_name)
    safe_file_name = safe_file_name.replace(" ", "_")

    current_timestamp = int(time.time())
    safe_file_name = f"{safe_file_name}-{current_timestamp}{file_extension}"
    safe_file_name = safe_file_name.lower()

    return safe_file_name
