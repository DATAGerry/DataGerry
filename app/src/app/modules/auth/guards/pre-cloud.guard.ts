import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { environment } from 'src/environments/environment';

export const preCloudGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);

  if (!environment.preCloudMode) {
    router.navigate(['/error/404']); 
    return false;
  }

  return true;
};
