import { Component, OnInit } from '@angular/core';

import { Employee } from '../../interfaces/employee.interface'
import { EmployeeService } from '../../services/employee.service'

@Component({
  selector: 'app-list-page',
  templateUrl: './list-page.component.html',
  styles: ``
})
export class ListPageComponent implements OnInit {
  public employees: Employee[] = []

  constructor( private employeeService: EmployeeService ){}

  ngOnInit(): void {
    this.employeeService.getEmployee()
      .subscribe( employees => this.employees = employees)
  }
}
