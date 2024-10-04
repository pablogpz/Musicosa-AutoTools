from dataclasses import dataclass

@dataclass
class Template:
    uuid: str
    entry_title: str

@dataclass
class StageFourInput:
    templates_api_url: str
    artifacts_folder: str
    templates: list[Template]
    retry_attempts: int
    overwrite: bool = False


@dataclass
class StageFourOutput:
    generated_templates: list[str] | None
    failed_templates_uuids: list[str] | None
