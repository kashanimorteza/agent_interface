// Regenerate src/lib/api/schema.d.ts from the running Backend's OpenAPI description.
import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";

const base = (process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/+$/, "");
const url = `${base}/openapi.json`;
const out = "src/lib/api/schema.d.ts";
const require = createRequire(import.meta.url);
const packageJson = require.resolve("openapi-typescript/package.json");
const cli = join(dirname(packageJson), require(packageJson).bin["openapi-typescript"]);
const result = spawnSync(process.execPath, [cli, url, "-o", out], { stdio: "inherit" });
if (result.status !== 0) {
  console.error(`openapi-typescript failed for ${url}; is the Backend running?`);
  process.exit(result.status ?? 1);
}
console.log(`generated ${out} from ${url}`);
