// API Access — the only Frontend boundary onto the application's contract.
//
// The lowest of the three responsibilities in this layer. Everything the
// interface knows about the application comes through here, in shapes derived
// from the contract's own description. Nothing above it makes a request.

export { APPLICATION_ADDRESS, Refused, Unreachable, ask } from "./client";
export { changeBody, creationBody, differs } from "./changes";
export type { Entered, Value } from "./changes";
export {
  changeRecord,
  createRecord,
  listRecords,
  readRecord,
  removeRecord,
  setRecordStatus,
} from "./operations";
export type { Page, Record_ } from "./operations";
export { RESOURCES, resourceAt } from "./contract/catalogue";
export type { FieldDescription, ResourceDescription, ReturnedField } from "./contract/catalogue";
