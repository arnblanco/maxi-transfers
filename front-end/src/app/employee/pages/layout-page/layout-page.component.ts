import { Component } from '@angular/core';

@Component({
  selector: 'app-layout-page',
  templateUrl: './layout-page.component.html',
  styles: ``
})
export class LayoutPageComponent {
  public sidebarItems = [
    { label: 'List', icon: 'label', url: './list'},
    { label: 'Add New', icon: 'add', url: './new-employee'}
  ]
}
