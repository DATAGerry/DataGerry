import { ValidatorFn, AbstractControl, ValidationErrors } from "@angular/forms";

export function uniqueCalculationBasisValidator(existingValues: number[], currentValue?: number): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    if (!control.value) return null;
    const valueFloat = parseFloat(control.value);
    if (isNaN(valueFloat)) return null;
    // Allow unchanged value in edit mode.
    if (currentValue !== undefined && valueFloat === currentValue) {
      return null;
    }
    return existingValues.includes(valueFloat) ? { duplicateCalculationBasis: true } : null;
  };
}