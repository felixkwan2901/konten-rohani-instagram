// Records real phone-size footage of the diam.dan.percaya site for the promo reel.
// node record.mjs  -> clips/*.mp4 (CFR 30fps, 780x1688)
import { createRequire } from 'module';
import { execFileSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const require = createRequire(import.meta.url);
const puppeteer = require('/Users/felixkwan/.npm/_npx/0affc4ee22ee6416/node_modules/puppeteer-core');
const CHROME = '/Users/felixkwan/.cache/hyperframes/chrome/chrome-headless-shell/mac_arm-152.0.7977.30/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const BASE = 'http://localhost:8081/diam.dan.percaya/';
const OUT = path.resolve('clips');
const sleep = ms => new Promise(r => setTimeout(r, ms));
fs.mkdirSync(OUT, { recursive: true });

async function record(page, name, fn) {
  const dir = path.join(OUT, name + '_frames');
  fs.rmSync(dir, { recursive: true, force: true });
  fs.mkdirSync(dir);
  const cdp = await page.createCDPSession();
  const frames = [];
  cdp.on('Page.screencastFrame', async f => {
    const file = path.join(dir, String(frames.length).padStart(5, '0') + '.jpg');
    fs.writeFileSync(file, Buffer.from(f.data, 'base64'));
    frames.push({ file, t: f.metadata.timestamp });
    cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }).catch(() => {});
  });
  await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 90, everyNthFrame: 1 });
  const t0 = Date.now() / 1000;
  await fn();
  const t1 = Date.now() / 1000;
  await cdp.send('Page.stopScreencast');
  await sleep(200);
  // Variable-rate frames -> concat list with real durations -> constant 30fps mp4.
  const lines = [];
  frames.forEach((f, i) => {
    const next = i + 1 < frames.length ? frames[i + 1].t : t1;
    lines.push(`file '${f.file}'`, `duration ${Math.max(0.001, next - f.t).toFixed(4)}`);
  });
  lines.push(`file '${frames[frames.length - 1].file}'`);
  const list = path.join(dir, 'list.txt');
  fs.writeFileSync(list, lines.join('\n'));
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list,
    '-vf', 'fps=30,scale=780:1688:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow',
    path.join(OUT, name + '.mp4')]);
  console.log(name, frames.length, 'frames', (t1 - t0).toFixed(1) + 's');
}

async function drag(page, x0, y0, x1, y1, ms) {
  await page.mouse.move(x0, y0);
  await page.mouse.down();
  const steps = Math.round(ms / 16);
  for (let i = 1; i <= steps; i++) {
    const k = i / steps, e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
    await page.mouse.move(x0 + (x1 - x0) * e, y0 + (y1 - y0) * e);
    await sleep(16);
  }
  await page.mouse.up();
}

const browser = await puppeteer.launch({
  executablePath: CHROME, headless: 'shell',
  args: ['--autoplay-policy=no-user-gesture-required', '--hide-scrollbars', '--force-color-profile=srgb']
});
const page = await browser.newPage();
await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2 });

/* A: intro -> sphere reveal -> drag -> open a card */
await page.goto(BASE, { waitUntil: 'networkidle2' });
await page.waitForSelector('#skip', { visible: true });
await page.waitForFunction(() => !document.getElementById('splash'), { timeout: 15000 });
await sleep(600);
await record(page, 'a_sphere', async () => {
  await page.click('#skip');
  await sleep(3200);
  await drag(page, 90, 470, 300, 430, 1300);
  await sleep(2200);
  await drag(page, 300, 520, 120, 500, 1000);
  await sleep(1800);
  const r = await page.evaluate(() => {
    let best = null, bd = 1e9;
    document.querySelectorAll('.card').forEach(c => {
      const b = c.getBoundingClientRect(), d = Math.hypot(b.x + b.width / 2 - 195, b.y + b.height / 2 - 470);
      if (+c.style.opacity > .9 && d < bd) { bd = d; best = { x: b.x + b.width / 2, y: b.y + b.height / 2 }; }
    });
    return best;
  });
  if (r) { await page.mouse.click(r.x, r.y); }
  await sleep(2600);
});

/* B: folder chips -> sphere swaps -> grid sections */
await page.keyboard.press('Escape');
await sleep(900);
await record(page, 'b_folders', async () => {
  await sleep(400);
  await page.click('[data-set="02"]');
  await sleep(1900);
  await page.click('[data-set="reels"]');
  await sleep(1900);
  await page.click('#menuBtn');
  await sleep(1300);
  await page.click('[data-grid]');
  await sleep(1600);
  for (let i = 0; i < 26; i++) { await page.mouse.wheel({ deltaY: 38 }); await sleep(40); }
  await sleep(1400);
});

/* C: Roti Hidup */
await page.goto(BASE + 'roti.html', { waitUntil: 'networkidle2' });
await page.evaluate(() => { try { localStorage.clear(); } catch (_) {} });
await page.reload({ waitUntil: 'networkidle2' });
await sleep(800);
await record(page, 'c_roti', async () => {
  await sleep(1300);
  await page.click('#loaf');
  await sleep(3600);
  await page.click('#again');
  await sleep(1400);
  await page.click('#loaf');
  await sleep(3200);
});

/* D: Stand Firm */
await page.goto(BASE + 'stand-firm.html', { waitUntil: 'networkidle2' });
await sleep(900);
await page.click('#btnBegin');
await sleep(400);
const cell = await page.evaluate(() => { const r = document.getElementById('game').getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; });
const at = (c, r) => [cell.x + (c + .5) / 14 * cell.w, cell.y + (r + .5) / 10 * cell.h];
await record(page, 'd_standfirm', async () => {
  await sleep(500);
  for (const [c, r] of [[3, 2], [5, 5], [7, 4]]) {
    await page.keyboard.press('1');
    await sleep(250);
    await page.mouse.click(...at(c, r));
    await sleep(450);
  }
  await page.keyboard.press('Space');
  await sleep(300);
  await page.keyboard.press('f');
  await sleep(6500);
});

await browser.close();
