// main.ts -- entrypoint for the news-image-20261120 entry.
//
// The front page is rendered ahead of time by render.py (deterministic,
// no network) and shipped in this repository as entry.png. This program
// only validates that image against the competition gate -- a whole PNG,
// exactly 1024x1024, at most 1 MiB -- and copies it to the output
// directory. It uses the Node 22 standard library only.

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;
const MAX_BYTES = 1024 * 1024;

// The PNG file signature: 137 80 78 71 13 10 26 10.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

// Read the image that ships beside this file.
const here = new URL(".", import.meta.url).pathname;
const sourcePath = join(here, "entry.png");
let bytes: Buffer;
try {
  bytes = readFileSync(sourcePath);
} catch {
  fail(`cannot read ${sourcePath}`);
}

if (bytes.length > MAX_BYTES) {
  fail(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
if (bytes.length < 33 || !bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  fail("entry.png does not start with the PNG signature");
}

// A PNG's IHDR chunk holds width and height as big-endian uint32s at
// offsets 16 and 20. Check the chunk really is IHDR first.
if (bytes.toString("ascii", 12, 16) !== "IHDR") {
  fail("entry.png has no IHDR chunk where one is expected");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
  fail(`entry.png is ${width}x${height}, expected ${EXPECTED_WIDTH}x${EXPECTED_HEIGHT}`);
}

// Copy the validated image to the output directory.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, "entry.png");
copyFileSync(sourcePath, outPath);
const written = statSync(outPath).size;
console.log(`main.ts: wrote ${outPath} (${width}x${height}, ${written} bytes)`);
