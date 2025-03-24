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


export function numericOrDecimalValidator(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const value = control.value;

    if (value === null || value === '') {
      return null;
    }

    const isValid = !isNaN(value) && /^-?\d+(\.\d+)?$/.test(value.toString());
    return isValid ? null : { invalidNumber: true };
  };
}



export function nonZeroValidator(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const value = parseFloat(control.value);
    if (!isNaN(value) && value === 0) {
      return { zeroNotAllowed: true };
    }
    return null;
  };
}
