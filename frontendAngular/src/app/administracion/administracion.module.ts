import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AgregarLibroComponent } from '../administracion/pages/agregar-libro/agregar-libro.component';
import { EditarLibroComponent } from '../administracion/pages/editar-libro/editar-libro.component';
import { AgregarAutoComponent } from '../administracion/pages/agregar-auto/agregar-auto.component';
import { CombinarAutoComponent } from '../administracion/pages/combinar-auto/combinar-auto.component';
import { PrimeNgModule } from '../prime-ng/prime-ng.module';
import { SharedModule } from '../shared/shared.module';
import { PanelAdminComponent } from './pages/panel-admin/panel-admin.component';
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms';
import { GestionCatalogoComponent } from './pages/gestion-catalogo/gestion-catalogo.component';
import { GestionUsuarioComponent } from './pages/gestion-usuario/gestion-usuario.component';
import { GestionRolesComponent } from './pages/gestion-roles/gestion-roles.component';
import { GestionEstimadorComponent } from './pages/gestion-estimador/gestion-estimador.component';
import { PermisosRolesComponent } from './pages/permisos-roles/permisos-roles.component';
import { EstimacionesGuardadasComponent } from './pages/estimaciones-guardadas/estimaciones-guardadas.component';

@NgModule({
  declarations: [
    AgregarLibroComponent,
    EditarLibroComponent,
    AgregarAutoComponent,
    CombinarAutoComponent,
    PanelAdminComponent,
    GestionCatalogoComponent,
    GestionUsuarioComponent,
    GestionRolesComponent,
    GestionEstimadorComponent,
    PermisosRolesComponent,
    EstimacionesGuardadasComponent
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
