/**
 * news-image-20261122 v2 (evening edition) — copy ./entry.png to the
 * output directory.
 *
 * Deterministic: byte-for-byte copy, so repeated runs produce identical
 * output. Node 22, stdlib only, no network.
 */
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";

// Validate the bundled image before copying: it must be a real PNG
// (8-byte magic 89 50 4E 47 0D 0A 1A 0A) and at most 1 MiB, so a corrupt
// or oversized file fails loudly instead of producing bad output.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1_048_576;
const size = statSync(src).size;
if (size > MAX_BYTES) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB cap`);
}
const header = readFileSync(src).subarray(0, 8);
if (!header.equals(PNG_MAGIC)) {
  throw new Error("entry.png does not start with the PNG magic bytes");
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
