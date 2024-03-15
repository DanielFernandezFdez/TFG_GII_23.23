import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InicioComponent } from './aplicacion/pages/inicio/inicio.component';
import { CatalogoComponent } from './aplicacion/pages/catalogo/catalogo.component';
import { AgregarLibroComponent } from './aplicacion/pages/agregar-libro/agregar-libro.component';
import { EditarLibroComponent } from './aplicacion/pages/editar-libro/editar-libro.component';
import { AgregarAutoComponent } from './aplicacion/pages/agregar-auto/agregar-auto.component';
import { EditarAutoComponent } from './aplicacion/pages/editar-auto/editar-auto.component';
import { CombinarAutoComponent } from './aplicacion/pages/combinar-auto/combinar-auto.component';
import { InfoLibroComponent } from './aplicacion/pages/info-libro/info-libro.component';


const routes: Routes = [
  {
    path: '',
    component: InicioComponent,
    pathMatch: 'full'
  },
  {
    path: 'catalogo',
    component: CatalogoComponent,
    pathMatch: 'full'
  },
  {
    path: 'info_libro/:id',
    component: InfoLibroComponent,
    pathMatch: 'full'
  },
  {
    path: 'agregar',
    component: AgregarLibroComponent,
    pathMatch: 'full'
  },
  {
    path: 'editar/:id',
    component: EditarLibroComponent,
    pathMatch: 'full'
  },
  {
    path: 'agregar_auto',
    component: AgregarAutoComponent,
    pathMatch: 'full'
  },
  {
    path: 'editar_auto/:id',
    component: EditarAutoComponent,
    pathMatch: 'full'
  },
  {
    path: 'combinar_auto',
    component: CombinarAutoComponent,
    pathMatch: 'full'
  }


];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
