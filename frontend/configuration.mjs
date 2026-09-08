// The settings this layer owns, and the binding the composition declares for it.
//
// Read once, on the server, before anything is served. Where the application is
// reached is a binding rather than a value written into the interface, so
// pointing the composition somewhere else and restarting is all it takes.

import { readFileSync, existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { parse } from "yaml";

const LAYER_ROOT = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = dirname(LAYER_ROOT);

export const SETTINGS_VARIABLE = "MY_FRONTEND_SETTINGS";
export const PUBLIC_VARIABLE = "MY_FRONTEND_PUBLIC_CONFIGURATION";

function documentAt(path) {
  if (!path || !existsSync(path)) return {};
  const loaded = parse(readFileSync(path, "utf8"));
  return loaded && typeof loaded === "object" ? loaded : {};
}

export function settingsFile() {
  const delivered = process.env[SETTINGS_VARIABLE];
  return delivered ? resolve(delivered) : join(LAYER_ROOT, "frontend.yaml");
}

export function publicFile() {
  const delivered = process.env[PUBLIC_VARIABLE];
  return delivered ? resolve(delivered) : join(PROJECT_ROOT, "application.yaml");
}

export function loadConfiguration() {
  const owned = documentAt(settingsFile()).settings ?? {};
  const declared = documentAt(publicFile()).frontend?.bindings ?? {};

  return {
    service: {
      host: owned.service?.host ?? "127.0.0.1",
      port: Number(owned.service?.port ?? 3000),
    },
    listing: {
      pageSize: Number(owned.listing?.page_size ?? 25),
    },
    appearance: {
      colorMode: owned.appearance?.color_mode ?? "system",
      direction: owned.appearance?.direction ?? "auto",
    },
    bindings: {
      // Where the application's contract is. Absent means the composition has
      // not said, which is a thing to report rather than to guess at.
      application: declared.backend?.address ?? null,
    },
  };
}
