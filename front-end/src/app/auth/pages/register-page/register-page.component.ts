import { Component } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';
import { UserRegister } from '../../interfaces/user.interface'

@Component({
  selector: 'app-register-page',
  templateUrl: './register-page.component.html',
  styles: ``
})
export class RegisterPageComponent {
  public registerForm = new FormGroup({
    first_name: new FormControl<string>(''),
    last_name: new FormControl<string>(''),
    email: new FormControl<string>(''),
    username: new FormControl<string>(''),
    password: new FormControl<string>(''),
  })

  constructor(
    private authService: AuthService,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private snackbar: MatSnackBar,
    private dialog: MatDialog
  ){}

  get currentRegister(): UserRegister {
    const user = this.registerForm.value as UserRegister
    return user
  }

  onSubmit(): void {

    if( this.registerForm.invalid ) {
      this.showSnackbar('Enter the requested values!')
      return
    }

    this.authService.signup( this.currentRegister )
      .subscribe( user_register => {
        this.router.navigate(['/auth/login'])
        this.showSnackbar(`${ user_register.username } user is register!`)
      })
  }

  showSnackbar( message: string ): void {
    this.snackbar.open( message, 'done', {
      duration: 2500
    })
  }

}
