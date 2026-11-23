// Entry for make.fun news-image-20261123: "Sum up 23 November's world news
// in one image". Node 22, standard library only, no network.
//
// The front page itself is drawn by draw.py (Pillow, flat editorial art with
// crisp vector text) and shipped in this repository as entry.png. This program
// just writes those exact bytes to /output/entry.png, so both grader runs
// produce identical output. Nothing here depends on time, randomness or the
// network, so the output is deterministic by construction. Run locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const outFile = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
writeFileSync(outFile, readFileSync(join(here, "entry.png")));
