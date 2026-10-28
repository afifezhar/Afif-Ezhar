const { chromium } = require('playwright');
// usage: render2.js html outDir fps dur [shard nShards | times=a,b,c]
const [,, html, outDir, fpsArg, durArg, a5, a6] = process.argv;
(async () => {
  const fps = +fpsArg, total = Math.round(fps * +durArg);
  let frames = [...Array(total).keys()];
  if (a5 && a5.startsWith('times=')) frames = a5.slice(6).split(',').map(s => Math.round(+s * fps));
  else if (a5) frames = frames.filter(f => f % +a6 === +a5);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + html, { waitUntil: 'load' });
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode())); });
  for (const f of frames) {
    await page.evaluate(t => window.render(t), f / fps);
    await page.screenshot({ path: `${outDir}/f${String(f).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 93 });
  }
  await browser.close();
})();
