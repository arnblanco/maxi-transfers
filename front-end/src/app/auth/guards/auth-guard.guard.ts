import { inject } from '@angular/core';
import { CanActivateFn, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';


export const AuthGuard: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  const router: Router = inject(Router)
  const protectedRoutes: string[] = ['/employee', '/employee/list', '/employee/new-employee', '/employee/:id']
  const session_active: boolean = (localStorage.getItem('token'))?true:false

  return protectedRoutes.includes(state.url) && !session_active
    ? router.navigate(['/auth/login'])
    : true
};
