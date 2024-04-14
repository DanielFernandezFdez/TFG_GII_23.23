import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InicioComponent } from './aplicacion/pages/inicio/inicio.component';
import { CatalogoComponent } from './aplicacion/pages/catalogo/catalogo.component';
import { AgregarLibroComponent } from './administracion/pages/agregar-libro/agregar-libro.component';
import { EditarLibroComponent } from './administracion/pages/editar-libro/editar-libro.component';
import { AgregarAutoComponent } from './administracion/pages/agregar-auto/agregar-auto.component';
import { CombinarAutoComponent } from './administracion/pages/combinar-auto/combinar-auto.component';
import { InfoLibroComponent } from './aplicacion/pages/info-libro/info-libro.component';
import { LoginComponent } from './aplicacion/pages/login/login.component';
import { EstimadorComponent } from './aplicacion/pages/estimador/estimador.component';
import { AuthGuard } from './auth/auth.guard';
import { PanelAdminComponent } from './administracion/pages/panel-admin/panel-admin.component';
import { GestionCatalogoComponent } from './administracion/pages/gestion-catalogo/gestion-catalogo.component';
import { GestionUsuarioComponent } from './administracion/pages/gestion-usuario/gestion-usuario.component';
import { GestionRolesComponent } from './administracion/pages/gestion-roles/gestion-roles.component';
import { GestionEstimadorComponent } from './administracion/pages/gestion-estimador/gestion-estimador.component';
import { PermisosRolesComponent } from './administracion/pages/permisos-roles/permisos-roles.component';


const routes: Routes = [
  {
    path: '',
    component: InicioComponent,
    pathMatch: 'full'
  },
  {
    path: 'catalogo',
    component: CatalogoComponent,
    pathMatch: 'full',
    //canActivate: [AuthGuard]  //Solo para pruebas
  },
  {
    path: 'info_libro/:id',
    component: InfoLibroComponent,
    pathMatch: 'full'
  },
  {
    path: 'agregar',
    component: AgregarLibroComponent,
    pathMatch: 'full',
    //canActivate: [AuthGuard]
  },
  {
    path: 'editar/:id',
    component: EditarLibroComponent,
    pathMatch: 'full',
    //canActivate: [AuthGuard]
  },
  {
    path: 'agregar_auto/:elemento',
    component: AgregarAutoComponent,
    pathMatch: 'full',
    //canActivate: [AuthGuard]
  },
  {
    path: 'combinar_auto',
    component: CombinarAutoComponent,
    pathMatch: 'full',
    //canActivate: [AuthGuard]
  },
  {
    path: 'login',
    component: LoginComponent,
    pathMatch: 'full'
  },
  {
    path: 'estimador',
    component: EstimadorComponent,
    pathMatch: 'full',
    //canActivate: [AuthGuard]
  },
  {
    path: 'panel-admin',
    component: PanelAdminComponent,
    pathMatch: 'full',
    //canActivate: [AuthGuard]
  },
  {
    path:'gestion-catalogo',
    component: GestionCatalogoComponent,
    pathMatch: 'full',
    //canActivate: [AuthGuard]
  },
  {
    path:'gestion-usuarios',
    component: GestionUsuarioComponent,
    pathMatch: 'full',
    canActivate: [AuthGuard]
  },
  {
    path:'gestion-roles',
    component: GestionRolesComponent,
    pathMatch: 'full',
    //canActivate: [AuthGuard]
  },
  {
    path:'gestion-estimador',
    component: GestionEstimadorComponent,
    pathMatch: 'full',
    //canActivate: [AuthGuard]
  },
  {
    path: 'gestion-permisos/:id',
    component:PermisosRolesComponent,
    pathMatch: 'full',
    //canActivate: [AuthGuard]
  }



];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
