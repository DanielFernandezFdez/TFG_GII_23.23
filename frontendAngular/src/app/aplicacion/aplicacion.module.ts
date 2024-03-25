import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { InicioComponent } from './pages/inicio/inicio.component';
import { CatalogoComponent } from './pages/catalogo/catalogo.component';
import { InfoLibroComponent } from './pages/info-libro/info-libro.component';
import { PrimeNgModule } from '../prime-ng/prime-ng.module';
import { SharedModule } from '../shared/shared.module';
import { LoginComponent } from './pages/login/login.component';
import { EstimadorComponent } from './pages/estimador/estimador.component';
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    InicioComponent,
    CatalogoComponent,
    InfoLibroComponent,
    LoginComponent,
    EstimadorComponent
  ],
  imports: [
    CommonModule,
    PrimeNgModule,
    SharedModule,
    ReactiveFormsModule,
    FormsModule
  ],
  exports: [
  ],
})
export class AplicacionModule { }
