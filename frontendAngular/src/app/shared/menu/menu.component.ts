import { Component } from '@angular/core';
import { MenuItem } from 'primeng/api';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrl: './menu.component.css'
})
export class MenuComponent {
  elem_izq: MenuItem[] =[];
  
  isLoggedIn: boolean = false;
  userName: string | null = '';
  
  constructor(public authService: AuthService) {
    if (this.authService.estaAutenticado()){
      this.isLoggedIn = true;
      this.userName = this.authService.usuarioActualValue;
    }
    }
  items: any[]=[];
  
  logout() {
    this.authService.logout();
  }
  ngOnInit() {
    this.authService.tokenValor.subscribe(token => {
      if (token) {
        this.items = [
          {
            label: 'Panel de Administrador',
            icon: 'pi pi-fw pi-cog',
            command: () => {
              // Acción para navegar al Panel de Administrador
            }
          },
          {
            label: 'Cerrar Sesión',
            icon: 'pi pi-fw pi-sign-out',
            command: () => this.logout()}];
      } 
    });
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

