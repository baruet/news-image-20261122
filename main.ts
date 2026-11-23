// main.ts — news-image-20261122 v3 (FINAL EDITION).
// Copies the rendered entry.png into the output directory.
// Deterministic: a plain byte copy, no timestamps, no network.
// Usage: node main.ts   (or: npx tsx main.ts)
// Output dir: $MAKEFUN_OUTPUT_DIR, default "/output".

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1 * 1024 * 1024; // competition cap: 1 MiB

const repoDir = dirname(fileURLToPath(import.meta.url));
const source = join(repoDir, "entry.png");
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
const dest = join(outDir, "entry.png");

const bytes = readFileSync(source);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG (bad magic bytes)");
}
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}
// IHDR chunk: width and height are big-endian uint32 at offsets 16 and 20.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 cap`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, dest);

const copied = statSync(dest);
const sha = createHash("sha256").update(readFileSync(dest)).digest("hex");
console.log(`wrote ${dest} (${copied.size} bytes, sha256 ${sha})`);
