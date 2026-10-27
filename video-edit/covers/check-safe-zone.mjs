// Fails if any overlay element in a cover leaves the shared social safe zone (../safe-zone.json).
// Usage: node check-safe-zone.mjs   (from video-edit/covers; set NODE_PATH=$(npm root -g) if playwright is global)
import { createRequire } from "node:module";
import { readFileSync, readdirSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const { chromium } = createRequire(import.meta.url)("playwright");

const zone = JSON.parse(readFileSync(new URL("../safe-zone.json", import.meta.url))).content;
// Overlay = anything that is not footage, shade or decorative full-height seam.
const OVERLAY = ".copy, .copy *, .chip, .pill";
const dir = resolve("compositions");
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
let failures = 0;
for (const file of readdirSync(dir).filter((f) => f.endsWith(".html")).sort()) {
  await page.goto(pathToFileURL(resolve(dir, file)).href);
  await page.evaluate(() => document.fonts.ready);
  const boxes = await page.$$eval(OVERLAY, (els) =>
    els.map((el) => {
      // Measure painted text, not the block box (a block div spans its full width).
      const r = document.createRange();
      r.selectNodeContents(el);
      const b = el.children.length ? el.getBoundingClientRect() : r.getBoundingClientRect();
      return { sel: el.className || el.tagName, x1: b.left, y1: b.top, x2: b.right, y2: b.bottom };
    }),
  );
  const bad = boxes.filter((b) => b.x1 < zone.x1 || b.y1 < zone.y1 || b.x2 > zone.x2 || b.y2 > zone.y2);
  const ext = boxes.reduce((a, b) => ({ x1: Math.min(a.x1, b.x1), y1: Math.min(a.y1, b.y1), x2: Math.max(a.x2, b.x2), y2: Math.max(a.y2, b.y2) }), { x1: 1e9, y1: 1e9, x2: 0, y2: 0 });
  const r = (n) => Math.round(n);
  console.log(`${bad.length ? "FAIL" : "ok  "} ${file}  overlay extent x ${r(ext.x1)}-${r(ext.x2)}, y ${r(ext.y1)}-${r(ext.y2)}`);
  for (const b of bad) console.log(`       ${b.sel}: x ${r(b.x1)}-${r(b.x2)}, y ${r(b.y1)}-${r(b.y2)}`);
  failures += bad.length;
}
await browser.close();
process.exit(failures ? 1 : 0);
