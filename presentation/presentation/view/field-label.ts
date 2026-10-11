import type { FieldDescription } from '@/interaction/fields'

/**
 * The name of a Field as a person reads it: the description its Declaration
 * gives, the same wherever the Field appears. A Field whose Declaration gives
 * no description is named by the words of its name ("user_id" reads "User id").
 */
export function fieldLabel(
  field: Pick<FieldDescription, 'name' | 'description'>,
): string {
  if (field.description !== undefined && field.description !== '') {
    return field.description
  }
  const words = field.name.replace(/_/g, ' ').trim()
  return words === ''
    ? field.name
    : words.charAt(0).toUpperCase() + words.slice(1)
}
