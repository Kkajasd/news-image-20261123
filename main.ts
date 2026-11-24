// news-image-20261123: copies the pre-rendered front-page PNG to the
// output directory. No network access, no dependencies beyond Node itself.
// The image sums up the world's news of Monday 23 November 2026.
//
// The copy is byte-exact and the program is fully deterministic: it reads
// one fixed file, validates the PNG gate (magic bytes, <= 1 MiB, exactly
// 1024x1024) and writes the same bytes to the output directory on every run.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const dest = join(outDir, "entry.png");
const MAX_BYTES = 1048576;

const buf = readFileSync(src);
if (buf.length < 8 || buf[0] !== 0x89 || buf[1] !== 0x50 || buf[2] !== 0x4e || buf[3] !== 0x47) {
  throw new Error("entry.png is not a PNG file (bad magic bytes)");
}
if (buf.length > MAX_BYTES) {
  throw new Error(`entry.png is ${buf.length} bytes, over the 1 MiB limit`);
}
// PNG IHDR: width at bytes 16-19, height at bytes 20-23 (big-endian).
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}

// Never remove the output directory (it may be a bind mount): only create it.
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
const copied = statSync(dest).size;
if (copied !== buf.length) {
  throw new Error(`copied size ${copied} does not match source size ${buf.length}`);
}
console.log(`Wrote ${dest} (${copied} bytes, ${width}x${height} PNG)`);
