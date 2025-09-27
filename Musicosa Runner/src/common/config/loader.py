import tomllib
from os import path

from common.config.config import Config, StageFiveConfig, StageFourConfig, StageOneConfig, StageSixConfig
from common.config.defaults import DEFAULT_CONFIG_FILE_NAME


def load_config(config_file: str | None = None) -> Config:
    if config_file is None:
        # When no config file is provided load the default from working dir
        if path.isfile(DEFAULT_CONFIG_FILE_NAME):
            config_file = DEFAULT_CONFIG_FILE_NAME
        # Else, try loading it from the parent folder
        elif path.isfile(f"../{DEFAULT_CONFIG_FILE_NAME}"):
            config_file = f"../{DEFAULT_CONFIG_FILE_NAME}"
        else:
            raise FileNotFoundError("Default config file not found in working directory or parent directory")
    elif not path.isfile(config_file):
        raise FileNotFoundError(f"Provided config file '{config_file}' not found")

    with open(config_file, "r") as config:
        try:
            config_contents = config.read()
        except IOError as err:
            raise IOError(f"Couldn't read config file contents. Cause: {err}") from err

    config_dict = tomllib.loads(config_contents, parse_float=float)

    try:
        return Config(
            start_from=config_dict["start_from"],
            artifacts_folder=config_dict["artifacts_folder"],
            stitch_final_video=config_dict["stitch_final_video"],
            stage_1=StageOneConfig(**config_dict["stage_1"]),
            stage_4=StageFourConfig(**config_dict["stage_4"]),
            stage_5=StageFiveConfig(**config_dict["stage_5"]),
            stage_6=StageSixConfig(**config_dict["stage_6"]),
        )
    except TypeError as err:
        raise TypeError(f"Couldn't parse config file. Cause: {err}") from err
