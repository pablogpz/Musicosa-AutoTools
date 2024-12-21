from os import path
from os.path import basename

from playwright.sync_api import Response, sync_playwright

from common.constants import TEMPLATE_IMG_FORMAT
from common.model.settings import get_setting_by_key
from common.naming.slugify import slugify
from stage_4_templates_gen.type_definitions import Template


def generate_all_templates(api_url: str,
                           templates: list[Template],
                           artifacts_folder: str,
                           retry_attempts: int,
                           overwrite: bool = False) -> tuple[list[str] | None, list[str] | None]:
    generated_templates: list[str] = []
    failed_templates_uuids: list[str] = []

    template_width: int = get_setting_by_key("templates.total_width_px").value
    template_height: int = get_setting_by_key("templates.total_height_px").value

    def load_template_page(url: str) -> Response:
        print(f"[LOADING TEMPLATE] {url}")
        return page.goto(url)

    def take_screenshot(path: str) -> None:
        print(f"[GENERATING TEMPLATE] {basename(path)}")
        page.screenshot(path=path, full_page=True)
        generated_templates.append(template.entry_title)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": template_width, "height": template_height})

        for template in templates:

            template_path = f"{artifacts_folder}/{slugify(template.entry_title)}.{TEMPLATE_IMG_FORMAT}"
            template_url = f"{api_url}/{template.uuid}"

            if not overwrite and path.isfile(template_path):
                print(f"[SKIPPING GENERATION] {template.entry_title}")
                continue

            response = load_template_page(template_url)

            if response.status == 200:
                take_screenshot(template_path)
            elif response.status == 404:
                print(f"[TEMPLATE NOT FOUND] {template.entry_title}")
                failed_templates_uuids.append(template.uuid)
            else:
                print(f"[GENERATION FAILED] {template} (HTTP status code: {response.status})")
                print(f"  Re-attempting to generate up to {retry_attempts} times")
                for attempt in range(1, retry_attempts + 1):

                    response = load_template_page(template_url)

                    if response.status == 200:
                        take_screenshot(template_path)
                        break

                    if attempt == retry_attempts:
                        failed_templates_uuids.append(template.uuid)

        browser.close()

    return generated_templates or None, failed_templates_uuids or None
