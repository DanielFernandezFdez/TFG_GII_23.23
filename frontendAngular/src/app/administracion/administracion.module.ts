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
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms';
import { GestionCatalogoComponent } from './pages/gestion-catalogo/gestion-catalogo.component';
import { GestionUsuarioComponent } from './pages/gestion-usuario/gestion-usuario.component';
import { GestionRolesComponent } from './pages/gestion-roles/gestion-roles.component';

import { EditarUsuarioComponent } from './pages/editar-usuario/editar-usuario.component';
import { AgregarUsuarioComponent } from './pages/agregar-usuario/agregar-usuario.component';
import { CambiarContraComponent } from './pages/cambiar-contra/cambiar-contra.component';
import { GestionEstimadorComponent } from './pages/gestion-estimador/gestion-estimador.component';

@NgModule({
  declarations: [
    AgregarLibroComponent,
    EditarLibroComponent,
    AgregarAutoComponent,
    EditarAutoComponent,
    CombinarAutoComponent,
    PanelAdminComponent,
    GestionCatalogoComponent,
    GestionUsuarioComponent,
    GestionRolesComponent,
    EditarUsuarioComponent,
    AgregarUsuarioComponent,
    CambiarContraComponent,
    GestionEstimadorComponent
    
  ],
  imports: [
    CommonModule,
    PrimeNgModule,
    SharedModule,
    ReactiveFormsModule,
    FormsModule
  ]
})
export class AdministracionModule { }
