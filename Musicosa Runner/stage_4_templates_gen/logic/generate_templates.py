from os import path
from os.path import basename

from playwright.sync_api import Response, sync_playwright

from common.constants import TEMPLATE_IMG_FORMAT, PRESENTATION_FILE_SUFFIX
from common.custom_types import TemplateType
from common.model.models import SettingKeys
from common.model.settings import get_setting_by_key
from common.naming.slugify import slugify
from stage_4_templates_gen.custom_types import Template
from stage_4_templates_gen.defaults import DEFAULT_OVERWRITE_TEMPLATES, DEFAULT_OVERWRITE_PRESENTATIONS


def generate_templates(templates_api_url: str,
                       presentations_api_url: str,
                       templates: list[Template],
                       artifacts_folder: str,
                       retry_attempts: int,
                       overwrite_templates: bool = DEFAULT_OVERWRITE_TEMPLATES,
                       overwrite_presentations: bool = DEFAULT_OVERWRITE_PRESENTATIONS
                       ) -> tuple[list[str] | None, list[str] | None]:
    generated_template_titles: list[str] = []
    failed_template_uuids: list[str] = []

    frame_width: int = get_setting_by_key(SettingKeys.FRAME_WIDTH_PX).value
    frame_height: int = get_setting_by_key(SettingKeys.FRAME_HEIGHT_PX).value

    def load_template_page(url: str) -> Response:
        print(f"[LOADING TEMPLATE] {url}")
        return page.goto(url)

    def take_screenshot(path: str) -> bool:
        print(f"[GENERATING TEMPLATE] {basename(path)}")
        page.screenshot(path=path, full_page=True)
        return True

    def generate_template(template_path: str, template_url: str, overwrite: bool) -> bool | None:
        if not overwrite and path.isfile(template_path):
            print(f"[SKIPPING GENERATION] {template.entry_title}")
            return None

        response = load_template_page(template_url)

        if response.status == 200:
            take_screenshot(template_path)
            return True
        elif response.status == 404:
            print(f"[TEMPLATE NOT FOUND] {template.entry_title}")
            return False
        else:
            print(f"[GENERATION FAILED] {template} (HTTP status code: {response.status})")
            print(f"  Re-attempting to generate up to {retry_attempts} times")

            for attempt in range(1, retry_attempts + 1):
                response = load_template_page(template_url)

                if response.status == 200:
                    take_screenshot(template_path)
                    return True

                if attempt == retry_attempts:
                    return False

        return False

    with sync_playwright() as p:
        browser = p.chromium.launch()
        # noinspection PyTypeChecker
        page = browser.new_page(viewport={"width": frame_width, "height": frame_height})

        for template in templates:
            entry_result = None
            presentation_result = None

            if TemplateType.ENTRY in template.types:
                template_path = f"{artifacts_folder}/{slugify(template.entry_title)}.{TEMPLATE_IMG_FORMAT}"
                template_url = f"{templates_api_url}/{template.uuid}"

                entry_result = generate_template(template_path, template_url, overwrite_templates)

            if TemplateType.PRESENTATION in template.types:
                template_path = \
                    f"{artifacts_folder}/{slugify(template.entry_title)}-{PRESENTATION_FILE_SUFFIX}.{TEMPLATE_IMG_FORMAT}"
                template_url = f"{presentations_api_url}/{template.uuid}"

                presentation_result = generate_template(template_path, template_url, overwrite_presentations)

            if entry_result is not None or presentation_result is not None:
                entry_result = entry_result if entry_result is not None else True
                presentation_result = presentation_result if presentation_result is not None else True

                if entry_result and presentation_result:
                    generated_template_titles.append(template.entry_title)
                else:
                    failed_template_uuids.append(template.uuid)

        browser.close()

    return generated_template_titles or None, failed_template_uuids or None
