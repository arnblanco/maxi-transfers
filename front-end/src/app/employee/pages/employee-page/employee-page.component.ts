import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { Employee, Beneficiaries } from '../../interfaces/employee.interface'
import { EmployeeService } from '../../services/employee.service'
import { forkJoin, switchMap, tap } from 'rxjs';


@Component({
  selector: 'app-employee-page',
  templateUrl: './employee-page.component.html',
  styles: ``
})
export class EmployeePageComponent implements OnInit {
  displayedColumns: string[] = ['first_name', 'last_name', 'curp', 'ssn', 'phone', 'percentage', 'actions'];
  public employee?: Employee;
  public beneficiaries?: Beneficiaries[];

  constructor(
    private employeeService: EmployeeService,
    private activatedRoute: ActivatedRoute,
    private router: Router
  ){}

  ngOnInit(): void {
    this.activatedRoute.params
      .pipe(
        switchMap(
          ({ id }) => forkJoin([
            this.employeeService.getEmployeeById( id ),
            this.employeeService.getEmployeeBeneficiaries( id )
          ])
        )
      )
      .subscribe(
        ([employee, beneficiaries]) => {
          this.employee = employee;
          this.beneficiaries = beneficiaries;
          return;
        }
      )
  }

  onRowClick(element: Beneficiaries): void {
    this.router.navigate(['/employee', element.employee_id, 'beneficiary', element.curp, 'edit' ]);
  }
}
