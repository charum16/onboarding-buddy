from __future__ import annotations

from typing import Any

import requests


class APIError(RuntimeError):
    """Readable error raised for failed API requests."""


class BuddyAPI:
    def __init__(self, base_url: str, timeout: int = 120) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        try:
            response = self.session.request(
                method,
                f"{self.base_url}{path}",
                timeout=self.timeout,
                **kwargs,
            )
        except requests.RequestException as exc:
            raise APIError(
                f"Can't reach the API at {self.base_url}. Check that the backend is running."
            ) from exc

        if not response.ok:
            try:
                detail = response.json().get("detail", response.text)
            except ValueError:
                detail = response.text or response.reason
            raise APIError(f"API error ({response.status_code}): {detail}")

        if response.status_code == 204 or not response.content:
            return None
        try:
            return response.json()
        except ValueError as exc:
            raise APIError("The API returned an unreadable response.") from exc

    def list_conversations(self) -> list[dict[str, Any]]:
        return self._request("GET", "/conversations")

    def create_conversation(self, name: str) -> dict[str, Any]:
        return self._request("POST", "/conversations", json={"convo_name": name})

    def delete_conversation(self, conversation_id: int) -> None:
        self._request("DELETE", f"/conversations/{conversation_id}")

    def get_messages(self, conversation_id: int) -> list[dict[str, Any]]:
        return self._request("GET", f"/conversations/{conversation_id}/messages")

    def send_message(self, conversation_id: int, content: str) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/conversations/{conversation_id}/messages",
            json={"content": content},
        )

    def upload_document(self, uploaded_file: Any, strategy: str) -> dict[str, Any]:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type or "application/octet-stream",
            )
        }
        return self._request(
            "POST",
            "/documents",
            params={"strategy": strategy},
            files=files,
        )
