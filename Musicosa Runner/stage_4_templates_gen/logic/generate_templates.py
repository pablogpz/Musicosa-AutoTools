from os import path
from os.path import basename

import playwright.sync_api
from playwright.sync_api import sync_playwright

from common.constants import TEMPLATE_IMG_FORMAT, PRESENTATION_IMG_FILE_SUFFIX
from common.custom_types import TemplateType
from common.formatting.tabulate import tab
from common.model.models import SettingKeys
from common.model.settings import get_setting_by_key
from common.naming.slugify import slugify
from stage_4_templates_gen.custom_types import TemplateGenerationResult, Template


def generate_templates(templates_api_url: str,
                       presentations_api_url: str,
                       templates: list[Template],
                       artifacts_folder: str,
                       retry_attempts: int,
                       overwrite_templates: bool,
                       overwrite_presentations: bool) -> tuple[TemplateGenerationResult, TemplateGenerationResult]:
    generated_nomination_template_titles: list[str] = []
    generated_presentation_template_titles: list[str] = []
    skipped_nomination_template_titles: list[str] = []
    skipped_presentation_template_titles: list[str] = []
    failed_nomination_template_ids: list[str] = []
    failed_presentation_template_ids: list[str] = []

    frame_width: int = get_setting_by_key(SettingKeys.FRAME_WIDTH_PX).value
    frame_height: int = get_setting_by_key(SettingKeys.FRAME_HEIGHT_PX).value

    def load_template_page(url: str, template_type: TemplateType) -> int:
        print(f"[LOADING #{idx + 1}] {template_type.name.upper()} {url}")
        try:
            return page.goto(url).status
        except playwright.sync_api.Error:
            return 0

    def take_screenshot(template_path: str, template_type: TemplateType) -> None:
        print(f"[GENERATING #{idx + 1}] {template_type.name.upper()} {basename(template_path)}")
        page.screenshot(path=template_path, full_page=True)

    def generate_template(template_path: str, url: str, template_type: TemplateType, overwrite: bool) -> bool | None:
        if not overwrite and path.isfile(template_path):
            print(f"[SKIPPING #{idx + 1}] {template_type.name.upper()} {template.friendly_name}")
            return None

        response = load_template_page(url, template_type)

        if response == 200:
            take_screenshot(template_path, template_type)
            return True
        elif response == 404:
            print(f"[FAILED #{idx + 1}] {template_type.name.upper()} Not found: {template.friendly_name}")
            return False
        else:
            print(f"[FAILED #{idx + 1}] {template_type.name.upper()} "
                  f"{template.friendly_name} (HTTP status code: {response})")
            print(tab(1, f"Re-attempting to generate up to {retry_attempts} times"))

            for attempt in range(1, retry_attempts + 1):
                response = load_template_page(url, template_type)

                if response == 200:
                    take_screenshot(template_path, template_type)
                    return True

                if attempt == retry_attempts:
                    return False

        return False

    with sync_playwright() as p:
        browser = p.chromium.launch()
        # noinspection PyTypeChecker
        page = browser.new_page(viewport={"width": frame_width, "height": frame_height})

        for idx, template in enumerate(templates):
            if TemplateType.NOMINATION in template.types:
                template_path = f"{artifacts_folder}/{slugify(template.friendly_name)}.{TEMPLATE_IMG_FORMAT}"
                template_url = f"{templates_api_url}/{template.id}"

                generation = generate_template(template_path, template_url, TemplateType.NOMINATION,
                                               overwrite_templates)

                if generation:
                    generated_nomination_template_titles.append(template.friendly_name)
                elif generation == False:
                    failed_nomination_template_ids.append(template.id)
                elif generation is None:
                    skipped_nomination_template_titles.append(template.friendly_name)

            if TemplateType.PRESENTATION in template.types:
                template_path = \
                    f"{artifacts_folder}/{slugify(template.friendly_name)}-{PRESENTATION_IMG_FILE_SUFFIX}.{TEMPLATE_IMG_FORMAT}"
                template_url = f"{presentations_api_url}/{template.id}"

                generation = generate_template(template_path, template_url, TemplateType.PRESENTATION,
                                               overwrite_presentations)

                if generation:
                    generated_presentation_template_titles.append(template.friendly_name)
                elif generation == False:
                    failed_presentation_template_ids.append(template.id)
                elif generation is None:
                    skipped_presentation_template_titles.append(template.friendly_name)

        browser.close()

    return (TemplateGenerationResult(generated_nomination_template_titles, skipped_nomination_template_titles,
                                     failed_nomination_template_ids),
            TemplateGenerationResult(generated_presentation_template_titles, skipped_presentation_template_titles,
                                     failed_presentation_template_ids))
