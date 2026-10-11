import { queryVocabulary as published } from './generated/vocabulary.ts'

/** An operator of a Filter and how many values it takes. */
export type OperatorForm = {
  readonly name: string
  readonly value: 'none' | 'one' | 'many'
}

/** The closed sets the API gives to listing, counting and aggregating. */
export type QueryVocabulary = {
  readonly operators: readonly OperatorForm[]
  readonly combinations: readonly string[]
  readonly directions: readonly string[]
}

export const queryVocabulary: QueryVocabulary = published
