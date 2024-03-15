import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MenubarModule } from 'primeng/menubar';
import { ButtonModule } from 'primeng/button';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { CardModule } from 'primeng/card';
import { InputTextModule } from 'primeng/inputtext';
import { FormsModule } from '@angular/forms';
import { RatingModule } from 'primeng/rating';
import { DividerModule } from 'primeng/divider';


@NgModule({
  declarations: [],
  imports: [
    CommonModule
  ],
  exports: [
    MenubarModule,
    BrowserAnimationsModule,
    ButtonModule,
    AutoCompleteModule,
    CardModule,
    InputTextModule,
    FormsModule,
    RatingModule,
    DividerModule
  ]
})
export class PrimeNgModule { }
