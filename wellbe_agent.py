"""
Core logic for the WellBe+ multi‑context AI assistant.

This module handles MCP server instantiation, model selection, and single‑shot
question answering. It is intentionally agnostic of any UI layer so that it can
be re‑used from a command‑line script, a notebook, or the Gradio front‑end.
"""

from __future__ import annotations

import asyncio
from copy import deepcopy
from typing import Tuple, Union

from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel
from agents.mcp.server import MCPServerStdio, MCPServerStreamableHttp

from config import PROMPT_TEMPLATE, MCP_CONFIGS

__all__ = [
    "build_mcp_servers",
    "select_model",
    "answer_question",
]


def build_mcp_servers(
    whoop_email: str, whoop_password: str
) -> Tuple[MCPServerStreamableHttp, MCPServerStdio]:
    """Return configured Healthcare and Whoop MCP servers.

    Parameters
    ----------
    whoop_email, whoop_password
        User credentials for the private Whoop feed. The credentials are merged
        into a *deep‑copied* variant of ``MCP_CONFIGS`` so that the global
        settings remain untouched.
    """
    cfg = deepcopy(MCP_CONFIGS)
    cfg["whoop"].update({"username": whoop_email, "password": whoop_password})

    healthcare_server = MCPServerStreamableHttp(
        params=cfg["healthcare-mcp-public"], name="Healthcare MCP Server"
    )
    whoop_server = MCPServerStdio(params=cfg["whoop"], name="Whoop MCP Server")
    return healthcare_server, whoop_server

def select_model() -> Union[str, LitellmModel]:
    return "o3-mini"


async def answer_question(
    question: str,
    openai_key: str,
    whoop_email: str,
    whoop_password: str,
) -> str:
    """Run the WellBe+ agent on a single question and return the assistant reply."""
    healthcare_srv, whoop_srv = build_mcp_servers(whoop_email, whoop_password)

    async with healthcare_srv as hserver, whoop_srv as wserver:
        agent = Agent(
            name="WellBe+ Assistant",
            instructions=PROMPT_TEMPLATE,
            model=select_model(),
            mcp_servers=[hserver, wserver],
        )
        result = await Runner.run(agent, question)
        return result.final_output


def answer_sync(question: str, openai_key: str, email: str, password: str) -> str:
    """Blocking wrapper around :func:`answer_question`."""
    if not question.strip():
        return "Please enter a question."
    try:
        return asyncio.run(
            answer_question(
                question, openai_key.strip(), email.strip(), password.strip()
            )
        )
    except Exception as exc:  # noqa: BLE001
        return f"**Error:** {exc}"
