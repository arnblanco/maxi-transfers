import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';

import { AuthService } from '../../services/auth.service';
import { UserLogin } from '../../interfaces/user.interface'


@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styles: ``
})
export class LoginPageComponent {
  public loginForm = new FormGroup({
    username: new FormControl<string>(''),
    password: new FormControl<string>(''),
  })

  constructor(
    private authService: AuthService,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private snackbar: MatSnackBar,
    private dialog: MatDialog
  ) {}

  get currentLogin(): UserLogin {
    const login_data = this.loginForm.value as UserLogin
    return login_data
  }

  onSubmit(): void {

    if( this.loginForm.invalid ) {
      this.showSnackbar('Enter the requested values!')
      return
    }

    this.authService.login( this.currentLogin )
      .subscribe( user_login => {
        this.router.navigate(['/'])
      })
  }

  showSnackbar( message: string ): void {
    this.snackbar.open( message, 'done', {
      duration: 2500
    })
  }
}
