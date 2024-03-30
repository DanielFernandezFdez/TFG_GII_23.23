import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InicioComponent } from './aplicacion/pages/inicio/inicio.component';
import { CatalogoComponent } from './aplicacion/pages/catalogo/catalogo.component';
import { AgregarLibroComponent } from './administracion/pages/agregar-libro/agregar-libro.component';
import { EditarLibroComponent } from './administracion/pages/editar-libro/editar-libro.component';
import { AgregarAutoComponent } from './administracion/pages/agregar-auto/agregar-auto.component';
import { EditarAutoComponent } from './administracion/pages/editar-auto/editar-auto.component';
import { CombinarAutoComponent } from './administracion/pages/combinar-auto/combinar-auto.component';
import { InfoLibroComponent } from './aplicacion/pages/info-libro/info-libro.component';
import { LoginComponent } from './aplicacion/pages/login/login.component';
import { EstimadorComponent } from './aplicacion/pages/estimador/estimador.component';
import { AuthGuard } from './auth/auth.guard';
import { PanelAdminComponent } from './administracion/pages/panel-admin/panel-admin.component';
import { GestionCatalogoComponent } from './administracion/pages/gestion-catalogo/gestion-catalogo.component';


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
    //canActivate: [AuthGuard]  Solo para pruebas
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
    path: 'agregar_auto',
    component: AgregarAutoComponent,
    pathMatch: 'full',
    //canActivate: [AuthGuard]
  },
  {
    path: 'editar_auto/:id',
    component: EditarAutoComponent,
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
  }


];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
