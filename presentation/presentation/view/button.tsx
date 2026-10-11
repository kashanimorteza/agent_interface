import type { ButtonHTMLAttributes } from 'react'
import styles from './button.module.css'

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary' | 'danger'
}

/** The one button every Component uses, so a button looks and behaves the same wherever it appears. */
export function Button({
  variant = 'secondary',
  className,
  type = 'button',
  ...rest
}: Props) {
  const classes = [styles.button, styles[variant], className]
    .filter(Boolean)
    .join(' ')
  return <button {...rest} type={type} className={classes} />
}
