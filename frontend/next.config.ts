import type { NextConfig } from "next";

import { loadConfiguration } from "./configuration.mjs";

// Read on the server, at the moment the layer starts, and handed to the browser
// as the address it should reach. It is a binding, not a secret: it says where
// the application is, and nothing about how to get into it.
const configuration = loadConfiguration();

const nextConfig: NextConfig = {
  env: {
    APPLICATION_ADDRESS: configuration.bindings.application ?? "",
    LISTING_PAGE_SIZE: String(configuration.listing.pageSize),
    APPEARANCE_COLOR_MODE: configuration.appearance.colorMode,
    APPEARANCE_DIRECTION: configuration.appearance.direction,
  },
};

export default nextConfig;
