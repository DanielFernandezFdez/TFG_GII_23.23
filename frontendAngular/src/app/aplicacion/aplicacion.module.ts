import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { InicioComponent } from './pages/inicio/inicio.component';
import { CatalogoComponent } from './pages/catalogo/catalogo.component';
import { InfoLibroComponent } from './pages/info-libro/info-libro.component';
import { AgregarLibroComponent } from './pages/agregar-libro/agregar-libro.component';
import { EditarLibroComponent } from './pages/editar-libro/editar-libro.component';
import { AgregarAutoComponent } from './pages/agregar-auto/agregar-auto.component';
import { EditarAutoComponent } from './pages/editar-auto/editar-auto.component';
import { CombinarAutoComponent } from './pages/combinar-auto/combinar-auto.component';
import { PrimeNgModule } from '../prime-ng/prime-ng.module';
import { SharedModule } from '../shared/shared.module';
import { LoginComponent } from './pages/login/login.component';




@NgModule({
  declarations: [
    InicioComponent,
    CatalogoComponent,
    InfoLibroComponent,
    AgregarLibroComponent,
    EditarLibroComponent,
    AgregarAutoComponent,
    EditarAutoComponent,
    CombinarAutoComponent,
    LoginComponent
  ],
  imports: [
    CommonModule,
    PrimeNgModule,
    SharedModule
  ],
  exports: [
  ],
})
export class AplicacionModule { }
