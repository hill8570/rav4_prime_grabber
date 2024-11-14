# Bypass the AWS WAF in front of the GraphQL endpoint.
from playwright.sync_api import sync_playwright


class WAFBypass:
    """Bypass the AWS WAF in front of the GraphQL endpoint."""

    def intercept_request(self, request):
        """Find the GraphQL request and save the headers."""
        if request.resource_type == "xhr" and request.url.endswith("/graphql"):
            self.valid_headers = request.headers
            # Just in case the request JSON is needed later.
            # pprint(request.post_data_json)
        return request

    def get_headers(self) -> None:
        """Run a browser to get valid headers for a WAF bypass."""
        with sync_playwright() as playwright:
            browser = playwright.firefox.launch(headless=True)
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()
            page.on("request", self.intercept_request)
            page.goto("https://www.toyota.com/search-inventory/model/rav4prime/?zipcode=83714")

            # # Debug: Print all input elements and their attributes
            # elements = page.evaluate('''() => {
            #     const inputs = document.querySelectorAll('input');
            #     return Array.from(inputs).map(el => ({
            #         id: el.id,
            #         name: el.name,
            #         class: el.className,
            #         type: el.type,
            #         placeholder: el.placeholder
            #     }));
            # }''')
            # print("Available input elements:", elements)
            #
            # # Debug: Print all elements with their text content
            # all_elements = page.evaluate('''() => {
            #     const all = document.querySelectorAll('*');
            #     return Array.from(all).map(el => ({
            #         tag: el.tagName,
            #         id: el.id,
            #         class: el.className,
            #         text: el.textContent.trim()
            #     })).filter(item => item.text);
            # }''')
            # print("All elements with text:", all_elements)

            # # Wait for ZIP input to be ready
            # page.wait_for_selector('input[inputPlaceholder="Enter ZIP"]', state='visible')
            # # Target ZIP input more specifically
            # zip_input = page.locator('input[inputPlaceholder="Enter ZIP"]').first
            # zip_input.click()
            # zip_input.fill("90210")
            # zip_input.press("Enter")
            page.wait_for_load_state("networkidle")
            browser.close()

    def run(self):
        """Return the valid headers to bypass the WAF."""
        self.get_headers()
        return self.valid_headers
