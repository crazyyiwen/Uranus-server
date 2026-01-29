"""Executor for HTTP request nodes."""

import asyncio
import json
from typing import Any, Dict

import requests

from BL.v3.nodes.executors.base_executor import BaseNodeExecutor


def _do_http_request(method: str, url: str, headers: Dict[str, Any], body: Dict[str, Any]) -> Any:
    """Sync HTTP request (run in executor)."""
    if method == "GET":
        return requests.get(url, headers=headers, timeout=30)
    if method == "POST":
        return requests.post(url, json=body, headers=headers, timeout=30)
    if method == "PUT":
        return requests.put(url, json=body, headers=headers, timeout=30)
    if method == "DELETE":
        return requests.delete(url, headers=headers, timeout=30)
    raise ValueError(f"Unsupported HTTP method: {method}")


class HttpRequestNodeExecutor(BaseNodeExecutor):
    """Executor for HTTP request nodes."""

    async def execute(self, node_config: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute HTTP request node (async).

        Args:
            node_config: HTTP request node configuration
            state: Current state

        Returns:
            HTTP response output
        """
        config = node_config.get("config", {})

        # Extract HTTP config
        url = config.get("url", "")
        method = config.get("method", "GET").upper()
        headers = config.get("headers", {})
        body = config.get("body", {})

        # Resolve templates in config
        url = self.variable_resolver.resolve(url, state)
        headers = {k: self.variable_resolver.resolve(v, state) for k, v in headers.items()}
        if isinstance(body, dict):
            body = {k: self.variable_resolver.resolve(v, state) for k, v in body.items()}

        # Make HTTP request in thread pool (requests is sync)
        try:
            response = await asyncio.to_thread(
                _do_http_request, method, url, headers, body
            )

            # Parse response
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = {"text": response.text}

            output = {
                "statusCode": response.status_code,
                "headers": dict(response.headers),
                "body": response_data,
            }
        except Exception as e:
            output = {
                "error": str(e),
                "statusCode": 500,
            }

        # Apply variable updates
        updated_state = self._apply_variable_updates(output, node_config, state)

        return {
            "output": output,
            "state": updated_state,
        }

    def get_output_schema(self) -> Dict[str, Any]:
        """Return output schema for HTTP request node."""
        return {
            "type": "object",
            "properties": {
                "statusCode": {"type": "integer"},
                "body": {"type": "object"},
            },
        }
