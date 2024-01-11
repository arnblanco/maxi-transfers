import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, catchError, of, map } from 'rxjs';

import { environment } from '../../../environment';

import { Employee, Beneficiaries } from '../interfaces/employee.interface';
import { Router } from '@angular/router';


@Injectable({providedIn: 'root'})
export class EmployeeService {
  private apiUrl: string = environment.apiUrl

  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      Authorization: `Bearer ${localStorage.getItem('token')}`
    });
  }

  private handleError(error: HttpErrorResponse): Observable<undefined> {
    if (error.status === 404) {
      this.router.navigate(['/404']);
    } else if (error.status === 401) {
      this.router.navigate(['/auth/login']);
    } else {
      this.router.navigate(['/404']);
    }
    return of(undefined);
  }

  constructor(
    private http: HttpClient,
    private router: Router
  ) { }

  getEmployee():Observable<Employee[]> {
    return this.http.get<Employee[]>(`${ this.apiUrl }/employee`, { headers: this.getHeaders() })
  }

  getEmployeeById(id: number): Observable<Employee | undefined> {
    return this.http.get<Employee>(`${this.apiUrl}/employee/${id}`, { headers: this.getHeaders() }).pipe(
      catchError((error: HttpErrorResponse) => this.handleError(error))
    );
  }

  addEmployee( employee:Employee ): Observable<Employee> {
    return this.http.post<Employee>(`${ this.apiUrl }/employee`, employee, { headers: this.getHeaders() })
  }

  updateEmployee( employee:Employee ): Observable<Employee> {
    return this.http.patch<Employee>(`${ this.apiUrl }/employee/${ employee.employee_id }`, employee, { headers: this.getHeaders() })
  }

  deleteEmployee( employee_id: number ): Observable<boolean> {
    return this.http.delete(`${ this.apiUrl }/employee/${ employee_id }`, { headers: this.getHeaders() })
      .pipe(
        map( resp => true ),
        catchError( err => of(false))
      )
  }

  getEmployeeBeneficiaries(id: number):Observable<Beneficiaries[]> {
    return this.http.get<Beneficiaries[]>(
      `${ this.apiUrl }/employee/${ id }/beneficiaries`, { headers: this.getHeaders() }
    )
  }

  getBeneficiary(employee_id: number, curp: string): Observable<Beneficiaries | undefined> {
    return this.http.get<Beneficiaries>(`${ this.apiUrl }/beneficiary/${ employee_id }/${ curp }`, { headers: this.getHeaders() })
      .pipe(
        catchError((error: HttpErrorResponse)=> {
          if(error.status === 404) {
            this.router.navigate(['/404'])
            return of(undefined)
          } else if (error.status === 401) {
            this.router.navigate(['/auth/login'])
            return of(undefined)
          } else {
            this.router.navigate(['/404'])
            return of(undefined)
          }
        })
      )
  }

  addBeneficiary( beneficiary:Beneficiaries ): Observable<Beneficiaries> {
    return this.http.post<Beneficiaries>(`${ this.apiUrl }/beneficiary`, beneficiary, { headers: this.getHeaders() })
  }

  patchBeneficiary( beneficiary:Beneficiaries ): Observable<Beneficiaries> {
    return this.http.patch<Beneficiaries>(`${ this.apiUrl }/beneficiary`, beneficiary, { headers: this.getHeaders() })
  }

  deleteBeneficiary( employee_id: number, curp: string ): Observable<boolean> {
    return this.http.delete(`${ this.apiUrl }/beneficiary/${ employee_id }/${ curp }`, { headers: this.getHeaders() })
      .pipe(
        map( resp => true ),
        catchError( err => of(false))
      )
  }
}
