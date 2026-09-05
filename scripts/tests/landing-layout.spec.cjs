const fs = require("node:fs");
const http = require("node:http");
const path = require("node:path");
const { test, expect } = require("@playwright/test");

const ROOT = path.resolve(__dirname, "../..");
const SITE = path.join(ROOT, "site");
const PREFIX = "/app-store-review-skill";

const VIEWPORTS = [
  { width: 320, height: 720 },
  { width: 390, height: 844 },
  { width: 768, height: 1024 },
  { width: 901, height: 900 },
  { width: 1024, height: 768 },
  { width: 1280, height: 800 },
  { width: 1440, height: 900 },
];

const FONT_FAILURE_VIEWPORTS = [
  { width: 320, height: 568 },
  { width: 390, height: 844 },
];

const MIME_TYPES = {
  ".avif": "image/avif",
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".webp": "image/webp",
  ".woff2": "font/woff2",
};

let server;
let landingUrl;

function resolveAsset(pathname) {
  if (pathname === PREFIX || pathname === `${PREFIX}/`) {
    return path.join(SITE, "index.html");
  }

  const relative = pathname.startsWith(`${PREFIX}/`)
    ? pathname.slice(PREFIX.length + 1)
    : "";
  const candidates = [
    path.join(SITE, relative),
    path.join(ROOT, relative),
  ];

  return candidates.find((candidate) => {
    const resolved = path.resolve(candidate);
    return (
      (resolved.startsWith(`${SITE}${path.sep}`) ||
        resolved.startsWith(`${ROOT}${path.sep}`)) &&
      fs.existsSync(resolved) &&
      fs.statSync(resolved).isFile()
    );
  });
}

test.beforeAll(async () => {
  server = http.createServer((request, response) => {
    let pathname;
    try {
      pathname = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
    } catch {
      response.writeHead(400).end("Bad request");
      return;
    }

    const asset = resolveAsset(pathname);
    if (!asset) {
      response.writeHead(404).end("Not found");
      return;
    }

    response.writeHead(200, {
      "Content-Type": MIME_TYPES[path.extname(asset)] || "application/octet-stream",
    });
    fs.createReadStream(asset).pipe(response);
  });

  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address();
  landingUrl = `http://127.0.0.1:${address.port}${PREFIX}/`;
});

test.afterAll(async () => {
  await new Promise((resolve, reject) => {
    server.close((error) => (error ? reject(error) : resolve()));
  });
});

for (const viewport of VIEWPORTS) {
  test(`landing geometry holds at ${viewport.width}px`, async ({ page }) => {
    await page.setViewportSize(viewport);
    await page.emulateMedia({ reducedMotion: "reduce" });

    const runtimeErrors = [];
    page.on("pageerror", (error) => runtimeErrors.push(error.message));
    page.on("console", (message) => {
      if (message.type() === "error") runtimeErrors.push(message.text());
    });

    const response = await page.goto(landingUrl, { waitUntil: "networkidle" });
    expect(response.status()).toBe(200);
    await page.evaluate(() => document.fonts.ready);

    await expect(page.locator(".campaign-hero")).toHaveCount(1);
    await expect(page.locator(".campaign-title")).toHaveCount(1);
    await expect(page.locator(".campaign-hero article, .campaign-hero aside")).toHaveCount(0);
    await expect(page.locator("body > .campaign-nav")).toHaveCount(1);
    await expect(page.locator(".campaign-nav a")).toHaveCount(2);
    await expect(page.getByRole("link", { name: "Report", exact: true })).toBeVisible();
    await expect(page.getByRole("link", { name: /GitHub/ })).toBeVisible();
    await expect(page.locator(".site-header, .brand")).toHaveCount(0);
    await expect(page.locator(".report-stage")).toHaveCount(1);

    const geometry = await page.evaluate(() => {
      const rect = (selector) => {
        const bounds = document.querySelector(selector).getBoundingClientRect();
        return {
          top: bounds.top,
          right: bounds.right,
          bottom: bounds.bottom,
          left: bounds.left,
          width: bounds.width,
          height: bounds.height,
        };
      };
      const overlaps = (first, second) =>
        Math.min(first.right, second.right) - Math.max(first.left, second.left) > 1 &&
        Math.min(first.bottom, second.bottom) - Math.max(first.top, second.top) > 1;

      const hero = rect(".campaign-hero");
      const title = rect(".campaign-title");
      const callToAction = rect(".button-primary");
      const navigation = rect(".campaign-nav");
      const art = rect(".campaign-art");
      const reportImage = document.querySelector(".report-artifact img");
      const heroBackground = getComputedStyle(document.querySelector(".campaign-hero")).backgroundColor;
      const reportBackground = getComputedStyle(document.querySelector(".report-stage")).backgroundColor;
      const titleStyles = getComputedStyle(document.querySelector(".campaign-title"));
      const callToActionStyles = getComputedStyle(document.querySelector(".button-primary"));
      const titleVisualLineCount = Array.from(
        document.querySelectorAll(".campaign-title > span"),
      ).reduce((count, span) => {
        const range = document.createRange();
        range.selectNodeContents(span);
        return count + range.getClientRects().length;
      }, 0);

      return {
        overflow: Math.max(
          document.documentElement.scrollWidth,
          document.body.scrollWidth,
        ) - window.innerWidth,
        callToAction,
        callToActionBackground: callToActionStyles.backgroundColor,
        callToActionColor: callToActionStyles.color,
        callToActionInsideHero:
          callToAction.top >= hero.top - 1 &&
          callToAction.right <= hero.right + 1 &&
          callToAction.bottom <= hero.bottom + 1 &&
          callToAction.left >= hero.left - 1,
        callToActionOverlapsTitle: overlaps(callToAction, title),
        heroStartsAtViewportTop: Math.abs(hero.top) <= 1,
        navigationInsideViewport:
          navigation.top >= 0 &&
          navigation.right <= window.innerWidth + 1 &&
          navigation.bottom <= window.innerHeight + 1 &&
          navigation.left >= -1,
        navigationOverlapsTitle: overlaps(navigation, title),
        artCoversHero:
          art.width >= hero.width - 1 && art.height >= hero.height - 1,
        titleLineCount: document.querySelectorAll(".campaign-title > span").length,
        titleVisualLineCount,
        titleFont: titleStyles.fontFamily,
        titleTrackingEm:
          Number.parseFloat(titleStyles.letterSpacing) /
          Number.parseFloat(titleStyles.fontSize),
        bodyFont: getComputedStyle(document.body).fontFamily,
        themeSwitchIsVisible: heroBackground !== reportBackground,
        reportImageLoaded: reportImage.complete && reportImage.naturalWidth > 0,
      };
    });

    expect(runtimeErrors).toEqual([]);
    expect(geometry.overflow).toBeLessThanOrEqual(1);
    expect(geometry.callToAction.top).toBeGreaterThanOrEqual(0);
    expect(geometry.callToAction.bottom).toBeLessThanOrEqual(viewport.height + 1);
    expect(geometry.callToActionBackground).toBe("rgb(247, 248, 246)");
    expect(geometry.callToActionColor).toBe("rgb(16, 21, 30)");
    expect(geometry.callToActionInsideHero).toBe(true);
    expect(geometry.callToActionOverlapsTitle).toBe(false);
    expect(geometry.heroStartsAtViewportTop).toBe(true);
    expect(geometry.navigationInsideViewport).toBe(true);
    expect(geometry.navigationOverlapsTitle).toBe(false);
    expect(geometry.artCoversHero).toBe(true);
    expect(geometry.titleLineCount).toBe(2);
    expect(geometry.titleVisualLineCount).toBe(2);
    expect(geometry.titleFont).toContain("Campaign Display");
    expect(geometry.titleTrackingEm).toBeGreaterThanOrEqual(-0.02);
    expect(geometry.bodyFont).toContain("Geist Sans");
    expect(geometry.themeSwitchIsVisible).toBe(true);
    expect(geometry.reportImageLoaded).toBe(true);
  });
}

for (const viewport of FONT_FAILURE_VIEWPORTS) {
  test(`hero stays usable without webfonts at ${viewport.width}px`, async ({ page }) => {
    let blockedFontRequests = 0;
    await page.route("**/*.woff2", (route) => {
      blockedFontRequests += 1;
      return route.abort("failed");
    });
    await page.setViewportSize(viewport);
    await page.emulateMedia({ reducedMotion: "reduce" });

    const response = await page.goto(landingUrl, { waitUntil: "networkidle" });
    expect(response.status()).toBe(200);
    await page.evaluate(() => document.fonts.ready);

    const geometry = await page.evaluate(() => {
      const bounds = (element) => {
        const box = element.getBoundingClientRect();
        return {
          top: box.top,
          right: box.right,
          bottom: box.bottom,
          left: box.left,
        };
      };
      const textBounds = (element) => {
        const range = document.createRange();
        range.selectNodeContents(element);
        const box = range.getBoundingClientRect();
        return {
          top: box.top,
          right: box.right,
          bottom: box.bottom,
          left: box.left,
        };
      };
      const overlaps = (first, second) =>
        Math.min(first.right, second.right) - Math.max(first.left, second.left) > 1 &&
        Math.min(first.bottom, second.bottom) - Math.max(first.top, second.top) > 1;

      const hero = bounds(document.querySelector(".campaign-hero"));
      const title = bounds(document.querySelector(".campaign-title"));
      const callToAction = bounds(document.querySelector(".button-primary"));
      const titleLines = Array.from(
        document.querySelectorAll(".campaign-title > span"),
        textBounds,
      );

      return {
        overflow: Math.max(
          document.documentElement.scrollWidth,
          document.body.scrollWidth,
        ) - window.innerWidth,
        titleFitsHero: titleLines.every(
          (line) => line.left >= hero.left - 1 && line.right <= hero.right + 1,
        ),
        titleOverlapsCallToAction: overlaps(title, callToAction),
        callToActionVisible:
          callToAction.top >= 0 && callToAction.bottom <= window.innerHeight + 1,
      };
    });

    expect(blockedFontRequests).toBeGreaterThan(0);
    expect(geometry.overflow).toBeLessThanOrEqual(1);
    expect(geometry.titleFitsHero).toBe(true);
    expect(geometry.titleOverlapsCallToAction).toBe(false);
    expect(geometry.callToActionVisible).toBe(true);
  });
}
