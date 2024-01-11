import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { switchMap, filter, tap } from 'rxjs';

import { ConfirmDialogComponent } from '../../components/confirm-dialog/confirm-dialog.component'
import { Beneficiaries } from '../../interfaces/employee.interface'
import { EmployeeService } from '../../services/employee.service'
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'employee-new-beneficiary',
  templateUrl: 'new-beneficiary.component.html',
  styles: ``
})
export class NewBeneficiaryComponent implements OnInit {
  public editBenefeciary: boolean  = false;
  public beneficiaryForm = new FormGroup({
    first_name: new FormControl<string>(''),
    last_name: new FormControl<string>(''),
    employee_id: new FormControl<number>(0),
    birthday: new FormControl<string>(''),
    curp: new FormControl<string>(''),
    ssn: new FormControl<string>(''),
    phone: new FormControl<string>(''),
    nationality: new FormControl<string>(''),
    percentage: new FormControl<number>(0)
  })

  constructor(
    private employeeService: EmployeeService,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private snackbar: MatSnackBar,
    private dialog: MatDialog
  ) { }

  get currentBeneficiary(): Beneficiaries {
    const beneficiary = this.beneficiaryForm.value as unknown
    return beneficiary as Beneficiaries
  }

  ngOnInit() {
    this.activatedRoute.params
    .pipe(
      tap(({ id, curp }) => {
        if (this.router.url.includes('edit')) {
          this.employeeService.getBeneficiary(id, curp).subscribe(beneficiary => {
            this.beneficiaryForm.reset(beneficiary);
            this.editBenefeciary = true;
          });
        } else {
          this.beneficiaryForm.get('employee_id')?.setValue(id);
        }
      })
    )
    .subscribe();
  }

  onSubmit(): void {
    this.activatedRoute.params
    .pipe(
      tap(({ id }) => this.beneficiaryForm.get('employee_id')?.setValue(id))
    )
    .subscribe();

    if(this.editBenefeciary) {
      this.employeeService.patchBeneficiary( this.currentBeneficiary )
        .subscribe( benefeciary => {
          this.showSnackbar(`${ benefeciary.first_name } ${ benefeciary.last_name } is updated!`)
        })

        return;
    }

    this.employeeService.addBeneficiary( this.currentBeneficiary )
      .subscribe( beneficiary => {
        this.router.navigate(['/employee', beneficiary.employee_id ])
        this.showSnackbar(`${ beneficiary.first_name } ${ beneficiary.last_name } beneficiary is created!`)
      })
  }

  onDeleteBeneficiary() {
    if( !this.editBenefeciary ) throw Error('Beneficiary is required!')

    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: this.beneficiaryForm.value
    })

    dialogRef.afterClosed()
      .pipe(
        filter( (result: boolean) => result ),
        switchMap( ()=> this.employeeService.deleteBeneficiary( this.currentBeneficiary.employee_id, this.currentBeneficiary.curp ) ),
        filter( (wasDeleted: boolean) => wasDeleted )
      )
      .subscribe(() => {
        this.router.navigate(['/employee', this.currentBeneficiary.employee_id])
      }
    )
  }

  showSnackbar( message: string ): void {
    this.snackbar.open( message, 'done', {
      duration: 2500
    })
  }
}
