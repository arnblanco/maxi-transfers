import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { switchMap, filter } from 'rxjs';

import { ConfirmDialogComponent } from '../../components/confirm-dialog/confirm-dialog.component'
import { Employee } from '../../interfaces/employee.interface'
import { EmployeeService } from '../../services/employee.service'
import { MatDialog } from '@angular/material/dialog';



@Component({
  selector: 'app-new-page',
  templateUrl: './new-page.component.html',
  styles: ``
})
export class NewPageComponent implements OnInit {
  public editEmployee: boolean  = false;
  public employeeForm = new FormGroup({
    first_name: new FormControl<string>(''),
    last_name: new FormControl<string>(''),
    birthday: new FormControl<Date>(new Date('1990-01-01')),
    employee_id: new FormControl<number>(0),
    curp: new FormControl<string>(''),
    ssn: new FormControl<string>(''),
    phone: new FormControl<string>(''),
    nationality: new FormControl<string>('')
  })

  constructor(
    private employeeService: EmployeeService,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private snackbar: MatSnackBar,
    private dialog: MatDialog
  ){}

  get currentEmployee(): Employee {
    const employee = this.employeeForm.value as Employee
    return employee
  }

  onSubmit(): void {

    if( this.employeeForm.invalid ) {
      this.showSnackbar('Enter the requested values!')
      return
    }

    if(this.editEmployee) {
      this.employeeService.updateEmployee( this.currentEmployee )
        .subscribe( employee => {
          this.showSnackbar(`${ employee.first_name } ${ employee.last_name } is updated!`)
        })

        return;
    }

    this.employeeService.addEmployee( this.currentEmployee )
      .subscribe( employee => {
        this.router.navigate(['/employee/edit', employee.employee_id ])
        this.showSnackbar(`${ employee.first_name } ${ employee.last_name } is created!`)
      })
  }

  ngOnInit(): void {
    if( !this.router.url.includes('edit')) return

    this.activatedRoute.params
      .pipe(
        switchMap( ({ id }) => this.employeeService.getEmployeeById( id ) ),
      ). subscribe( employee => {
        this.employeeForm.reset( employee )
        console.log(this.employeeForm.value)
        this.editEmployee = true
        return;
      })
  }

  onDeleteEmployee() {
    if( !this.editEmployee ) throw Error('Employee ID is required!')

    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: this.employeeForm.value
    })

    dialogRef.afterClosed()
      .pipe(
        filter( (result: boolean) => result ),
        switchMap( ()=> this.employeeService.deleteEmployee( this.currentEmployee.employee_id ) ),
        filter( (wasDeleted: boolean) => wasDeleted )
      )
      .subscribe(() => {
        this.router.navigate(['/employee'])
      }
    )
  }

  showSnackbar( message: string ): void {
    this.snackbar.open( message, 'done', {
      duration: 2500
    })
  }
}
