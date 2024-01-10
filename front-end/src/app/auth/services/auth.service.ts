import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap, of } from 'rxjs';

import { environment } from '../../../environment';
import { UserToken, UserRegister, UserLogin } from '../interfaces/user.interface'


@Injectable({providedIn: 'root'})
export class AuthService {

  private apiUrl: string = environment.apiUrl
  private user?: UserToken;

  constructor(private http: HttpClient) { }

  get currentUser(): UserToken|undefined {
    if( !this.user ) return undefined
    return structuredClone( this.user )
  }

  login( login:UserLogin ):Observable<UserToken>{
    return this.http.post<UserToken>(`${ this.apiUrl }/auth/login`, login)
      .pipe(
        tap( user => this.user = user),
        tap( user => localStorage.setItem('token', user.access_token))
      )
  }

  signup( user:UserRegister ): Observable<UserRegister> {
    return this.http.post<UserRegister>(`${ this.apiUrl }/auth/signup`, user)
  }

  checkAuthentication(): Observable<boolean> | boolean {
    if(!localStorage.getItem('token')) return false

    return of(true)
  }

  logout(): void {
    this.user = undefined
    localStorage.clear()
  }
}
