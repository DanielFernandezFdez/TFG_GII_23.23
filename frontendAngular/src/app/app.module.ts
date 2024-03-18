import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SharedModule } from './shared/shared.module';
import { AplicacionModule } from './aplicacion/aplicacion.module';
import { RouterModule } from '@angular/router';

;

@NgModule({
  declarations: [
    AppComponent

  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RouterModule,
    SharedModule,
    AplicacionModule,
    HttpClientModule,
   
  ],

  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
