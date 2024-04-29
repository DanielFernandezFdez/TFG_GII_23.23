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
import { SplitButtonModule } from 'primeng/splitbutton';
import { CheckboxModule } from 'primeng/checkbox';
import { SidebarModule } from 'primeng/sidebar';
import { AccordionModule } from 'primeng/accordion';
import { KnobModule } from 'primeng/knob';
import { StepsModule } from 'primeng/steps';
import { MultiSelectModule } from 'primeng/multiselect';
import {InputNumberModule} from 'primeng/inputnumber';
import { RadioButtonModule } from 'primeng/radiobutton';
import { DropdownModule } from 'primeng/dropdown';
import { ScrollTopModule } from 'primeng/scrolltop';
import { TableModule } from 'primeng/table';
import { PaginatorModule } from 'primeng/paginator';
import { PanelMenuModule } from 'primeng/panelmenu';
import { OverlayPanelModule } from 'primeng/overlaypanel';
import { InputSwitchModule } from 'primeng/inputswitch';
import { ChartModule } from 'primeng/chart';
import { CalendarModule } from 'primeng/calendar';

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
    DividerModule,
    SplitButtonModule,
    CheckboxModule,
    SidebarModule,
    AccordionModule,
    KnobModule,
    StepsModule,
    MultiSelectModule,
    InputNumberModule,
    RadioButtonModule,
    DropdownModule,
    ScrollTopModule,
    TableModule,
    PaginatorModule,
    PanelMenuModule,
    OverlayPanelModule,
    InputSwitchModule,
    ChartModule,
    CalendarModule
  ]
})
export class PrimeNgModule { }
