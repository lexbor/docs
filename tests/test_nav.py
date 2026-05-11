"""
Visual tests for docs nav/header.
Source of truth: docs/source/_templates/page.html inline styles.
"""
import os
import re

import pytest
from playwright.sync_api import Page, expect


EXPECTED_NAV_ITEMS = [
    "Download",
    "Documentation",
    "Support",
    "License",
    "Developers",
    "GitHub",
]

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")


def _goto(page: Page, url: str) -> None:
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_selector(".head", timeout=10000)


@pytest.fixture(autouse=True)
def ensure_screenshots_dir():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def test_head_background_color(page: Page, docs_server: str):
    _goto(page, docs_server)
    head = page.locator(".head")
    bg = head.evaluate("el => getComputedStyle(el).backgroundColor")
    assert bg == "rgb(50, 56, 65)", f"Expected #323841 (rgb(50, 56, 65)), got {bg}"


def test_head_left_background_color(page: Page, docs_server: str):
    _goto(page, docs_server)
    head_left = page.locator(".head-left")
    bg = head_left.evaluate("el => getComputedStyle(el).backgroundColor")
    assert bg == "rgb(41, 46, 54)", f"Expected #292e36 (rgb(41, 46, 54)), got {bg}"


def test_head_left_link_color(page: Page, docs_server: str):
    _goto(page, docs_server)
    link = page.locator(".head-left a")
    color = link.evaluate("el => getComputedStyle(el).color")
    assert color == "rgb(175, 184, 190)", f"Expected #afb8be (rgb(175, 184, 190)), got {color}"


def test_nav_link_color(page: Page, docs_server: str):
    _goto(page, docs_server)
    first_nav_link = page.locator(".head-right ul li a").first
    color = first_nav_link.evaluate("el => getComputedStyle(el).color")
    assert color == "rgb(255, 255, 255)", f"Expected #fff (rgb(255, 255, 255)), got {color}"


def test_head_font_size(page: Page, docs_server: str):
    _goto(page, docs_server)
    head = page.locator(".head")
    font_size = head.evaluate("el => getComputedStyle(el).fontSize")
    assert font_size == "14px", f"Expected 14px, got {font_size}"


def test_nav_items_count(page: Page, docs_server: str):
    _goto(page, docs_server)
    items = page.locator(".head-right ul li a")
    count = items.count()
    assert count == len(EXPECTED_NAV_ITEMS), (
        f"Expected {len(EXPECTED_NAV_ITEMS)} nav items, got {count}"
    )


def test_nav_items_text(page: Page, docs_server: str):
    _goto(page, docs_server)
    items = page.locator(".head-right ul li a")
    actual = [items.nth(i).inner_text().strip() for i in range(items.count())]
    assert actual == EXPECTED_NAV_ITEMS, f"Nav items mismatch: {actual}"


def test_head_smoke_screenshot(page: Page, docs_server: str):
    page.route(re.compile(r"^https?://(?!127\.0\.0\.1)"), lambda r: r.abort())
    _goto(page, docs_server)
    head = page.locator(".head")
    box = head.bounding_box()
    assert box is not None, ".head element has no bounding box"
    page.screenshot(
        path=os.path.join(SCREENSHOTS_DIR, "nav_smoke.png"),
        clip={"x": box["x"], "y": box["y"], "width": box["width"], "height": box["height"]},
    )
