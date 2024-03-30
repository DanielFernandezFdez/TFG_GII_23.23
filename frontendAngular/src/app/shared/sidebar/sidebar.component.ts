import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Router } from '@angular/router';

interface Pantalla {
  nombre: string;
  ruta: string;
  icono:string;
}

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent {
  @Input() visible: boolean = false;
  @Output() visibleChange = new EventEmitter<boolean>();
  pantallasGenerales: Pantalla[] = [
    { 
      nombre: 'Inicio', 
      ruta: '/' , 
      icono: 'pi pi-home'
    },
    { 
      nombre: 'Catálogo', 
      ruta: '/catalogo', 
      icono: 'pi pi-list'  
    },
    {
      nombre: 'Guía de análisis',
      ruta: '/',
      icono: 'pi pi-fw pi-info-circle',
      
    },
    {
      nombre: 'Decálogo',
      ruta: '/',
      icono: 'pi pi-bars',
     
    },
    {
      nombre: 'Referentes',
      ruta: '/',
      icono: 'pi pi-bookmark-fill',

    },
    {
      nombre: 'Guía de puntuación',
      ruta: '/',
      icono: 'pi pi-fw pi-info-circle',

    },
    {
      nombre: 'Valoración',
      ruta: '/estimador',
      icono: 'pi pi-fw pi-calculator',

    },

  ];
  usuario: Pantalla[] = [
    {
      nombre: 'Gestión de usuarios',
      ruta: '/',
      icono: 'pi pi-user-edit',
    },
    {
      nombre: 'Gestión de roles',
      ruta: '/',
      icono: 'pi pi-eye-slash',
    },
  ];
    catalogo: Pantalla[] = [
      {
        nombre: 'Agregar Libro manual',
        ruta: '/agregar',
        icono: 'pi pi-plus',
      },
      {
        nombre: 'Agregar Libro auto',
        ruta: '/',
        icono: 'pi pi-send',
      },
      {
        nombre: 'Gestionar Catálogo',
        ruta: '/gestion-catalogo',
        icono: 'pi pi-book',
      },
      {
        nombre: 'Importación y exportación',
        ruta: '/',
        icono: 'pi pi-upload',
      },
  ];


  constructor(private router: Router) { }

  seleccionar(ruta: string) {
    this.router.navigate([ruta]);
    this.cerrarSidebar();
  }

  cerrarSidebar() {
    this.visible = false;
    this.visibleChange.emit(this.visible);
  }
}