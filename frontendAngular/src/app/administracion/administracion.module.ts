import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AgregarLibroComponent } from '../administracion/pages/agregar-libro/agregar-libro.component';
import { EditarLibroComponent } from '../administracion/pages/editar-libro/editar-libro.component';
import { AgregarAutoComponent } from '../administracion/pages/agregar-auto/agregar-auto.component';
import { EditarAutoComponent } from '../administracion/pages/editar-auto/editar-auto.component';
import { CombinarAutoComponent } from '../administracion/pages/combinar-auto/combinar-auto.component';
import { PrimeNgModule } from '../prime-ng/prime-ng.module';
import { SharedModule } from '../shared/shared.module';
import { PanelAdminComponent } from './pages/panel-admin/panel-admin.component';


@NgModule({
  declarations: [
    AgregarLibroComponent,
    EditarLibroComponent,
    AgregarAutoComponent,
    EditarAutoComponent,
    CombinarAutoComponent,
    PanelAdminComponent
  ],
  imports: [
    CommonModule,
    PrimeNgModule,
    SharedModule
  ]
})
export class AdministracionModule { }
