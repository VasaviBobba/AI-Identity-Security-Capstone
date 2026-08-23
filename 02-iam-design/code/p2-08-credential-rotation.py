import os
import time
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUDIENCE = os.getenv("AUTH0_AUDIENCE")

TOKEN_URL = f"https://{DOMAIN}/oauth/token"
CHAT_URL = "http://localhost:3000/chat"


def timestamp():
    return datetime.now(timezone.utc).astimezone().strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )


def get_token():
    print(f"[{timestamp()}] Requesting M2M access token...")

    response = requests.post(
        TOKEN_URL,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "audience": AUDIENCE,
        },
        timeout=20,
    )

    print(f"[{timestamp()}] Token endpoint HTTP status: {response.status_code}")

    response.raise_for_status()

    data = response.json()

    token = data["access_token"]
    expires_in = data.get("expires_in")

    print(f"[{timestamp()}] Token received.")
    print(f"[{timestamp()}] expires_in = {expires_in} seconds")

    return token, expires_in


def call_chat(token, label):
    print(f"\n[{timestamp()}] {label}")
    print(f"[{timestamp()}] Calling {CHAT_URL} ...")

    response = requests.post(
        CHAT_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "message": "P2-08 credential rotation test"
        },
        timeout=20,
    )

    print(f"[{timestamp()}] HTTP {response.status_code}")

    try:
        print(f"[{timestamp()}] Response: {response.json()}")
    except Exception:
        print(f"[{timestamp()}] Response: {response.text}")

    return response.status_code


def main():
    if not all([DOMAIN, CLIENT_ID, CLIENT_SECRET, AUDIENCE]):
        raise RuntimeError(
            "Missing AUTH0_DOMAIN, AUTH0_CLIENT_ID, "
            "AUTH0_CLIENT_SECRET, or AUTH0_AUDIENCE in .env"
        )

    token, expires_in = get_token()

    if expires_in != 60:
        print(
            f"\nWARNING: Auth0 returned expires_in={expires_in}, "
            "not 60 seconds."
        )

    first_status = call_chat(
        token,
        "FIRST REQUEST — fresh M2M token"
    )

    if first_status != 200:
        print(
            f"\nERROR: Expected 200 from first /chat call, "
            f"but received {first_status}."
        )
        return

    print("\n" + "=" * 70)
    print(f"[{timestamp()}] Waiting for token expiration...")
    print(f"[{timestamp()}] Waiting 65 seconds...")
    print("=" * 70)

    time.sleep(65)

    second_status = call_chat(
        token,
        "SECOND REQUEST — replaying expired M2M token"
    )

    if second_status == 401:
        print("\n" + "=" * 70)
        print("P2-08 RESULT: PASS")
        print("Fresh token -> 200 OK")
        print("Expired token replay -> 401 Unauthorized")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("P2-08 RESULT: NOT CONFIRMED")
        print(f"Expected 401 after expiry, received {second_status}")
        print("=" * 70)


if __name__ == "__main__":
    main()