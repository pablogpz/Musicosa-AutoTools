from os import path
from os.path import basename

from playwright.sync_api import Response, sync_playwright

from common.constants import TEMPLATE_IMG_FORMAT, PRESENTATION_FILE_SUFFIX
from common.model.settings import get_setting_by_key
from common.naming.slugify import slugify
from common.type_definitions import TemplateType
from stage_4_templates_gen.defaults import DEFAULT_OVERWRITE_TEMPLATES, DEFAULT_OVERWRITE_PRESENTATIONS
from stage_4_templates_gen.type_definitions import Template


def generate_all_templates(templates_api_url: str,
                           presentations_api_url: str,
                           templates: list[Template],
                           artifacts_folder: str,
                           retry_attempts: int,
                           overwrite_templates: bool = DEFAULT_OVERWRITE_TEMPLATES,
                           overwrite_presentations: bool = DEFAULT_OVERWRITE_PRESENTATIONS
                           ) -> tuple[list[str] | None, list[str] | None]:
    generated_templates: list[str] = []
    failed_templates_uuids: list[str] = []

    frame_width: int = get_setting_by_key("frame.width_px").value
    frame_height: int = get_setting_by_key("frame.height_px").value

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
        page = browser.new_page(viewport={"width": frame_width, "height": frame_height})

        for template in templates:
            template_result = None
            presentation_result = None

            if TemplateType.ENTRY in template.template_targets:
                template_path = f"{artifacts_folder}/{slugify(template.entry_title)}.{TEMPLATE_IMG_FORMAT}"
                template_url = f"{templates_api_url}/{template.uuid}"

                template_result = generate_template(template_path, template_url, overwrite_templates)

            if TemplateType.PRESENTATION in template.template_targets:
                template_path = \
                    f"{artifacts_folder}/{slugify(template.entry_title)}-{PRESENTATION_FILE_SUFFIX}.{TEMPLATE_IMG_FORMAT}"
                template_url = f"{presentations_api_url}/{template.uuid}"

                presentation_result = generate_template(template_path, template_url, overwrite_presentations)

            if template_result is not None or presentation_result is not None:

                success = template_result if template_result is not None else True and presentation_result \
                    if presentation_result is not None else True

                if success:
                    generated_templates.append(template.entry_title)
                else:
                    failed_templates_uuids.append(template.uuid)

        browser.close()

    return generated_templates or None, failed_templates_uuids or None
