"""
Centralised, cached access to runtime configuration.
"""

from functools import lru_cache
from importlib import resources
import json
import os
from pathlib import Path
import yaml
from dotenv import load_dotenv


@lru_cache(maxsize=None)
def _load_prompt_template() -> str:
    with open("prompts/router_prompt.yml", "r") as fh:
        return yaml.safe_load(fh)["template"]


@lru_cache(maxsize=None)
def _load_mcp_configs() -> dict:
    cfg_path = Path(
        os.getenv(
            "MCP_CONFIG_PATH",
            Path(__file__).resolve().parent / "settings" / "mcp_config.json",
        )
    )
    with cfg_path.open() as fh:
        return json.load(fh)["mcpServers"]


load_dotenv()

PROMPT_TEMPLATE: str = _load_prompt_template()
MCP_CONFIGS: dict = _load_mcp_configs()
MODEL_API_KEY: str = os.getenv("MODEL_API_KEY")
