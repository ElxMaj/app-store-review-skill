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

      const hero = rect(".hero");
      const copy = rect(".hero-copy");
      const callToAction = rect(".button-primary");
      const report = rect(".hero-report-sheet");

      return {
        overflow: Math.max(
          document.documentElement.scrollWidth,
          document.body.scrollWidth,
        ) - window.innerWidth,
        callToAction,
        report,
        reportInsideHero:
          report.top >= hero.top - 1 &&
          report.right <= hero.right + 1 &&
          report.bottom <= hero.bottom + 1 &&
          report.left >= hero.left - 1,
        reportOverlapsCopy: overlaps(report, copy),
      };
    });

    expect(runtimeErrors).toEqual([]);
    expect(geometry.overflow).toBeLessThanOrEqual(1);
    expect(geometry.callToAction.top).toBeGreaterThanOrEqual(0);
    expect(geometry.callToAction.bottom).toBeLessThanOrEqual(viewport.height + 1);
    expect(geometry.report.width).toBeGreaterThan(0);
    expect(geometry.report.height).toBeGreaterThan(0);
    expect(geometry.reportInsideHero).toBe(true);
    expect(geometry.reportOverlapsCopy).toBe(false);
  });
}
