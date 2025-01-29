import { AbstractControl, ValidationErrors } from '@angular/forms';

// A stricter email regex that requires a dot + at least two chars
export function strictEmailValidator(control: AbstractControl): ValidationErrors | null {
  if (!control.value) {
    return null;
  }

  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  const isValid = pattern.test(control.value);

  return isValid ? null : { strictEmail: true };
}
