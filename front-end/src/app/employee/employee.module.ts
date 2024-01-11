import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MaterialModule } from '../material/material.module'

import { EmployeeRoutingModule } from './employee-routing.module';
import { EmployeePageComponent } from './pages/employee-page/employee-page.component';
import { LayoutPageComponent } from './pages/layout-page/layout-page.component';
import { ListPageComponent } from './pages/list-page/list-page.component';
import { NewPageComponent } from './pages/new-page/new-page.component';
import { NewBeneficiaryComponent } from './pages/new-beneficiary/new-beneficiary.component';
import { SearchPageComponent } from './pages/search-page/search-page.component';
import { CardComponent } from './components/card/card.component';
import { ConfirmDialogComponent } from './components/confirm-dialog/confirm-dialog.component';



@NgModule({
  declarations: [
    EmployeePageComponent,
    LayoutPageComponent,
    ListPageComponent,
    NewPageComponent,
    NewBeneficiaryComponent,
    SearchPageComponent,
    CardComponent,
    ConfirmDialogComponent
  ],
  imports: [
    CommonModule,
    EmployeeRoutingModule,
    MaterialModule
  ]
})

export class EmployeeModule { }
