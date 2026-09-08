// The appearance decisions, resolved once and read from the layer's settings.
//
// Whether the interface follows the reader's own preference or is fixed, and
// which way it reads, are decided here and consumed everywhere. Nothing
// rendered decides either for itself.

export type ColorMode = "system" | "light" | "dark";
export type Direction = "auto" | "ltr" | "rtl";

export const COLOR_MODE: ColorMode = (process.env.APPEARANCE_COLOR_MODE as ColorMode) || "system";
export const DIRECTION: Direction = (process.env.APPEARANCE_DIRECTION as Direction) || "auto";
export const PAGE_SIZE: number = Number(process.env.LISTING_PAGE_SIZE || 25);

/**
 * What the document should say about its appearance.
 *
 * Following the reader's preference means saying nothing and letting the visual
 * system's own light-and-dark rules apply; a fixed choice is stated so it wins.
 */
export function appearanceAttribute(mode: ColorMode = COLOR_MODE): string | undefined {
  return mode === "system" ? undefined : mode;
}

/** Which way the interface reads; letting the document decide when it is auto. */
export function directionAttribute(direction: Direction = DIRECTION): "ltr" | "rtl" | "auto" {
  return direction;
}
