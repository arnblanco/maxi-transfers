import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LayoutPageComponent } from './pages/layout-page/layout-page.component'
import { NewPageComponent } from './pages/new-page/new-page.component'
import { NewBeneficiaryComponent } from './pages/new-beneficiary/new-beneficiary.component';
import { SearchPageComponent } from './pages/search-page/search-page.component'
import { ListPageComponent } from './pages/list-page/list-page.component'
import { EmployeePageComponent } from './pages/employee-page/employee-page.component'

const routes: Routes = [
  {
    path: '',
    component: LayoutPageComponent,
    children: [
      {
        path: 'new-employee',
        component: NewPageComponent
      },
      {
        path: 'list',
        component: ListPageComponent
      },{
        path: 'edit/:id',
        component: NewPageComponent
      },
      {
        path: ':id',
        component: EmployeePageComponent
      },
      {
        path: ':id/beneficiary',
        component: NewBeneficiaryComponent
      },
      {
        path: ':id/beneficiary/:curp/edit',
        component: NewBeneficiaryComponent
      },
      {
        path: '**',
        redirectTo: 'list'
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EmployeeRoutingModule { }
