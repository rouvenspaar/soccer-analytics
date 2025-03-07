import os
from dotenv import load_dotenv

from event import load_events_from_json

if __name__ == "__main__":
    load_dotenv()
    json_file_path = os.getenv("JSON_FILE_PATH")

    if not json_file_path:
        raise ValueError("JSON_FILE_PATH is not set in .env file")

    events = load_events_from_json(json_file_path)
    print(events[0])
