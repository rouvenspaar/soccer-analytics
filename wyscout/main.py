import os
from dotenv import load_dotenv

from event import load_events_from_json

files = ["5574548", "5574557", "5662871", "5637448"] # 5684335 is missing

if __name__ == "__main__":
    load_dotenv()

    json_file_path = os.getenv("WYSCOUT_PATH")
    if not json_file_path:
        raise ValueError("WYSCOUT_PATH is not set in .env file")

    json_file_path += files[0]
    json_file_path += ".json"

    events = load_events_from_json(json_file_path)
    print(events[0])
