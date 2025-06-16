import json

import requests

from settings import ANKICONNECT_API_VERSION, ANKICONNECT_AUTH_TOKEN, ANKICONNECT_URL


class AnkiConnectService:
    def __init__(self, url: str, auth_token: str | None = None):
        self.url = url
        self.headers = {"Content-Type": "application/json"}
        if auth_token:
            self.headers["Authorization"] = f"Token {auth_token}"

    def _send_request(self, action: str, params: dict) -> dict:
        payload = json.dumps(
            {
                "action": action,
                "version": ANKICONNECT_API_VERSION,
                "params": params,
            }
        )
        try:
            response = requests.post(self.url, headers=self.headers, data=payload)
            response.raise_for_status()
            result = response.json()
            if result.get("error"):
                raise Exception(f"AnkiConnect Error: {result['error']}")
            return result["result"]
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to AnkiConnect: {e}")
        except json.JSONDecodeError:
            raise ValueError("AnkiConnect returned invalid JSON response.")
        except Exception as e:
            raise RuntimeError(f"AnkiConnect operation failed: {e}")

    def find_cards_in_deck(self, deck_name: str) -> list[int]:
        """Finds card IDs in a specific deck."""
        return self._send_request("findCards", {"query": f'deck:"{deck_name}"'})

    def get_cards_info(self, card_ids: list[int]) -> list[dict]:
        """Gets detailed information for a list of card IDs."""
        return self._send_request("cardsInfo", {"cards": card_ids})


# Singleton instance for easy import
anki_service = AnkiConnectService(
    url=ANKICONNECT_URL, auth_token=ANKICONNECT_AUTH_TOKEN
)
