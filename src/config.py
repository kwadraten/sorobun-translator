import json
from pathlib import Path
import os
from typing import Dict
import logging


Config = {
    "base_api": None,
    "base_key": None,
    "base_model": None,
    "reasoning_api": None,
    "reasoning_key": None,
    "reasoning_model": None,
    "mecab_dictionary_path": None,
    "logging_level": None,
    "database_path": None,
    "target_language": None
}

def level_convert(level: str | None) -> int:
    levels_dict = {
        "DEBUG": 10,
        "INFO": 20,
        "ERROR": 40,
    }
    if level:
        return levels_dict.get(level.upper(), 40)
    else:
        return 40



def initialize(
        config_path: Path | None = None, 
        inject: Dict[str, str] = {}
    ) -> None:
    if not config_path:
        config_path = Path(os.path.abspath(".")) / Path("config.json")
    with open(config_path, "rt", encoding="utf-8") as config_file:
        external_config = json.load(config_file)
    
    Config["base_api"] = external_config.get("base_api")
    Config["base_key"] = external_config.get("base_key")
    Config["base_model"] = external_config.get("base_model")
    Config["reasoning_api"] = external_config.get("reasoning_api")
    Config["reasoning_key"] = external_config.get("reasoning_key")
    Config["reasoning_model"] = external_config.get("reasoning_model")
    Config["mecab_dictionary_path"] = external_config.get("mecab_dictionary_path")
    Config["database_path"] = external_config.get("database_path")
    Config["target_language"] = external_config.get("target_language", "CHINESE")

    if inject.get("database_path"):
        Config["database_path"] = inject.get("database_path")
    if inject.get("target_language"):
        Config["target_language"] = inject.get("target_language", "CHINESE")
    
    # configure logging module
    level_str = external_config.get("logging_level")
    if inject.get("logging_level"):
        level_str = inject["logging_level"]
    logging.basicConfig(level=level_convert(level_str))