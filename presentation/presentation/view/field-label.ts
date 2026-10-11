/** The name of a Field as a person reads it: "user_id" becomes "User id". */
export function fieldLabel(name: string): string {
  const words = name.replace(/_/g, ' ').trim()
  return words === '' ? name : words.charAt(0).toUpperCase() + words.slice(1)
}
