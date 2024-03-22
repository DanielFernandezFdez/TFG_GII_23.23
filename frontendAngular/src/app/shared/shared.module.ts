import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MenuComponent } from './menu/menu.component';
import { FooterComponent } from './footer/footer.component';
import { PrimeNgModule } from '../prime-ng/prime-ng.module';
import { MenuDashboardComponent } from './menu-dashboard/menu-dashboard.component';
import { SidebarComponent } from './sidebar/sidebar.component';



@NgModule({
  declarations: [
    MenuComponent,
    FooterComponent,
    MenuDashboardComponent,
    SidebarComponent
  ],
  imports: [
    CommonModule,
    PrimeNgModule
  ],
  exports: [
    MenuComponent,
    FooterComponent,
    MenuDashboardComponent,
    SidebarComponent
  ]
})
export class SharedModule { }
