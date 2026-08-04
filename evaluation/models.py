#!/usr/bin/env python3
"""Model clients for the evaluation harness.

Two roles call a model: the *subject*, which reads a schema in isolation, and
the *supervisor*, which grades transcripts against a rubric. Both go through the
same interface so that they can be pointed at different models, which is the
point -- a supervisor that is the same model as the subject is grading itself.

Transports:

  openai   any OpenAI-compatible /chat/completions endpoint. Configured by
           EVAL_API_BASE (default https://api.openai.com/v1) and EVAL_API_KEY.
  none     records the prompt and returns nothing. Lets the whole harness be
           exercised, and every prompt inspected, without a key or a spend.

Only the standard library is used, deliberately: this harness has to be runnable
by a reviewer who wants to check the method, not only by its author.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass


class ModelError(RuntimeError):
    pass


@dataclass
class Response:
    text: str
    model: str
    prompt: str


class Client:
    def complete(self, system: str, user: str) -> Response:
        raise NotImplementedError


class NullClient(Client):
    """Returns an empty completion. Used to inspect prompts without calling out."""

    name = "none"

    def __init__(self, model: str = "none"):
        self.model = model

    def complete(self, system: str, user: str) -> Response:
        return Response(text="", model=self.model, prompt=f"{system}\n\n---\n\n{user}")


class OpenAIClient(Client):
    """Any OpenAI-compatible chat-completions endpoint."""

    name = "openai"

    def __init__(self, model: str, base: str | None = None, key: str | None = None,
                 temperature: float = 0.0, retries: int = 3, timeout: int = 600):
        self.model = model
        self.base = (base or os.environ.get("EVAL_API_BASE")
                     or "https://api.openai.com/v1").rstrip("/")
        self.key = key or os.environ.get("EVAL_API_KEY") or ""
        if not self.key:
            raise ModelError(
                "No API key. Set EVAL_API_KEY, or run with --transport none to "
                "build and inspect the prompts without calling a model."
            )
        self.temperature = temperature
        self.retries = retries
        self.timeout = timeout

    def complete(self, system: str, user: str) -> Response:
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base}/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.key}",
            },
            method="POST",
        )
        last: Exception | None = None
        for attempt in range(self.retries):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as handle:
                    document = json.loads(handle.read().decode("utf-8"))
                text = document["choices"][0]["message"]["content"] or ""
                return Response(text=text, model=self.model,
                                prompt=f"{system}\n\n---\n\n{user}")
            except (urllib.error.URLError, KeyError, ValueError) as error:
                last = error
                if attempt + 1 < self.retries:
                    time.sleep(2 ** attempt)
        raise ModelError(f"{self.model}: {last}")


def build(transport: str, model: str, **kwargs) -> Client:
    if transport == "none":
        return NullClient(model)
    if transport == "openai":
        return OpenAIClient(model, **kwargs)
    raise ModelError(f"unknown transport {transport!r}")
