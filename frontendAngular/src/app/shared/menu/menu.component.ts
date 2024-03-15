import { Component } from '@angular/core';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrl: './menu.component.css'
})
export class MenuComponent {
  elem_izq: MenuItem[] =[];
  

  ngOnInit() {
    this.elem_izq = [
      {
        label: 'Inicio',
        icon: 'pi pi-fw pi-home',
        routerLink: ['/']
      },
      {
        label: 'Catálogo',
        icon: 'pi pi-fw pi-book',
        routerLink: ['/catalogo']
      },
      {
        label: 'Guía de análisis',
        icon: 'pi pi-fw pi-info-circle',
        routerLink: ['/'],
      },
      {
        label: 'Decálogo',
        icon: 'pi pi-bars',
        routerLink: ['/'],
      },
      {
        label: 'Referentes',
        icon: 'pi pi-bookmark-fill',
        routerLink: ['/'],
      },
      {
        label: 'Guía de puntuación',
        icon: 'pi pi-fw pi-info-circle',
        routerLink: ['/'],
      }
     
    ];
    
    }
  }

