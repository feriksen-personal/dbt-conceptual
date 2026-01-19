#!/usr/bin/env python3
"""Generate PNG assets from readme-assets.html using Playwright."""

import asyncio
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: playwright not installed")
    print("Run: pip install playwright && playwright install chromium")
    exit(1)


async def generate_assets():
    """Generate PNG assets from HTML."""
    script_dir = Path(__file__).parent
    html_file = script_dir / "readme-assets.html"
    assets_dir = script_dir.parent.parent.parent / "assets"

    # Ensure assets directory exists
    assets_dir.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load the HTML file
        await page.goto(f"file://{html_file.absolute()}")

        # Wait for fonts to load
        await page.wait_for_timeout(1000)

        # Asset 1: Logo Banner Dark (800x140)
        print("Generating logo-banner-dark.png...")
        banner_dark = await page.query_selector(".logo-banner-dark")
        await banner_dark.screenshot(
            path=str(assets_dir / "logo-banner-dark.png"),
            omit_background=False
        )

        # Asset 3: Canvas Example (900x400)
        print("Generating canvas-example.png...")
        canvas = await page.query_selector(".canvas-example")
        await canvas.screenshot(
            path=str(assets_dir / "canvas-example.png"),
            omit_background=False
        )

        # Asset 4: UI Screenshot (1100x600)
        print("Generating ui-screenshot.png...")
        ui_screenshot = await page.query_selector(".ui-screenshot")
        await ui_screenshot.screenshot(
            path=str(assets_dir / "ui-screenshot.png"),
            omit_background=False
        )

        await browser.close()

    print(f"\nAssets generated in: {assets_dir}")
    print("- logo-banner-dark.png")
    print("- canvas-example.png")
    print("- ui-screenshot.png")


if __name__ == "__main__":
    asyncio.run(generate_assets())
