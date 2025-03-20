import json
import os
from io import StringIO
from pathlib import Path

import yaml


def find_files(directory, extension):
    for root, _, files in os.walk(directory, followlinks=True):
        for file in files:
            if file.endswith(extension):
                yield Path(root) / file


def load_config_from_directory(config_dir, env):
    print("Loading configuration from directory", config_dir)
    root_path = Path(config_dir)
    if not root_path.exists():
        raise FileNotFoundError(f"Configuration directory {root_path} not found")

    # look for all .json & .yaml & .yml files in the directory
    config_files = (
        list(find_files(root_path, ".json"))
        + list(find_files(root_path, ".yaml"))
        + list(find_files(root_path, ".yml"))
    )

    # resolve to absolute paths, deduplicate and sort alphabetically
    config_files = list(sorted(set(str(f.resolve()) for f in config_files)))

    # load the configuration files
    for cfg in config_files:
        print("  processing file", cfg)
        loaded_config_text = Path(cfg).read_text().lstrip()
        if loaded_config_text.startswith("{"):
            loaded_config = json.loads(loaded_config_text)
        else:
            loaded_config = yaml.safe_load(StringIO(loaded_config_text))
        for k, v in loaded_config.items():
            k = k.upper()
            if not k.startswith("INVENIO_"):
                k = f"INVENIO_{k}"
            print("    setting key ", k)
            env[k] = v

    print("Configuration loaded")
    return env
