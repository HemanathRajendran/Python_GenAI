from playwright.sync_api import sync_playwright
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()
    page.goto("https://www.cricbuzz.com/cricket-match/live-scores")

    page.wait_for_timeout(5000)

    page.screenshot(path="cricbuzz_score.png", full_page=True)

    text = page.locator("body").inner_text()

    # match = re.search(r"\d+\-\d+\s*\(\d+\.?\d*\)", text)
    match = re.findall(r'\d+(?:\s*&\s*\d+-\d+)?|\d+-\d+', text)

    if match:
        print("Live Score:", match[0])
    else:
        print("Score not found")

    browser.close()
