import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Employee } from '../../interfaces/employee.interface';


@Component({
  selector: 'employee-confirm-dialog',
  templateUrl: './confirm-dialog.component.html',
  styles: ``
})
export class ConfirmDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<ConfirmDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: Employee
  ){}

  onNoClick(): void {
    this.dialogRef.close(false)
  }

  deleteEmployee(): void {
    this.dialogRef.close(true)
  }
}
