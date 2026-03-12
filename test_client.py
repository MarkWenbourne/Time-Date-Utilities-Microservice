import requests

BASE_URL = "http://127.0.0.1:5002"

print("=== Normalize Datetime Test ===")

normalize_payload = {
    "dateTime": "2026-03-12 14:30",
    "sourceTimezone": "UTC"
}

r1 = requests.post(f"{BASE_URL}/normalize-datetime", json=normalize_payload)
print(r1.status_code)
print(r1.json())

print("\n=== Time Remaining Test ===")

remaining_payload = {
    "targetDateTime": "2026-03-20T12:00:00",
    "timezone": "UTC"
}

r2 = requests.post(f"{BASE_URL}/time-remaining", json=remaining_payload)
print(r2.status_code)
print(r2.json())