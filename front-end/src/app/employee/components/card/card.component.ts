import { Component, Input, OnInit } from '@angular/core';

import { Employee } from '../../interfaces/employee.interface'

@Component({
  selector: 'employee-employee-card',
  templateUrl: './card.component.html',
  styles: ``
})
export class CardComponent implements OnInit {

  @Input()
  public employee!: Employee;

  ngOnInit(): void {
    if( !this.employee ) throw Error('Employee property is required')
  }
}
