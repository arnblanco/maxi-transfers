import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { Employee } from '../../interfaces/employee.interface'
import { EmployeeService } from '../../services/employee.service'
import { switchMap } from 'rxjs';


@Component({
  selector: 'app-employee-page',
  templateUrl: './employee-page.component.html',
  styles: ``
})
export class EmployeePageComponent implements OnInit {
  public employee?: Employee;

  constructor(
    private employeeService: EmployeeService,
    private activatedRoute: ActivatedRoute,
    private router: Router
  ){}

  ngOnInit(): void {
    this.activatedRoute.params
      .pipe(
        switchMap(
          ({ id }) => this.employeeService.getEmployeeById( id )
        )
      )
      .subscribe(
        employee => {
          this.employee = employee
          return;
        }
      )
  }
}
