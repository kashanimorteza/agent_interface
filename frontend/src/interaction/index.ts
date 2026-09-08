// Interaction Logic — how the interface behaves.
//
// The middle of the three responsibilities in this layer. It holds what belongs
// to the experience rather than to the application: what is being looked at,
// what is being typed, and what the person is told while they wait. It reaches
// the application only through the door below it, and decides nothing the
// application decides.

export { idle, isEmpty, refusalFrom, refused, settled, working } from "./feedback";
export type { Progress, Refusal, Standing } from "./feedback";
export { useCreation, useRecord, useRecords } from "./use-records";
export type { Creation, Listing, OneRecord } from "./use-records";
export { useEntry } from "./use-entry";
export type { Entry } from "./use-entry";

// What the contract describes, passed on to the layer above. Presentation reads
// it from here rather than reaching the door itself: it is the same
// description, arriving by the way the layering allows.
export { RESOURCES, resourceAt } from "@/api-access";
export type {
  Entered,
  FieldDescription,
  Record_,
  ResourceDescription,
  ReturnedField,
  Value,
} from "@/api-access";
