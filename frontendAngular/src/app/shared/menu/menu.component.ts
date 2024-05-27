import { Component, ViewChild  } from '@angular/core';
import { MenuItem } from 'primeng/api';
import { AuthService } from '../../services/auth.service';

import Swal from 'sweetalert2'
import { Router } from '@angular/router';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent {


  elem_izq: MenuItem[] =[];
  
  isLoggedIn: boolean = false;
  userName: string | null = '';
  
  constructor(public authService: AuthService, private router: Router) {
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
              this.router.navigate(['/panel-admin'])
            }
          },
          {
            label: 'Cerrar Sesión',
            icon: 'pi pi-fw pi-sign-out',
            command: () => this.msgConfirmacionLogout()}];
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
        routerLink: ['/guia-analisis'],
      },
      {
        label: 'Decálogo',
        icon: 'pi pi-bars',
        routerLink: ['/decalogo'],
      },
      {
        label: 'Referentes',
        icon: 'pi pi-bookmark-fill',
        routerLink: ['/referentes'],
      },
      {
        label: 'Valoración',
        icon: 'pi pi-fw pi-calculator',
        routerLink: ['/estimador'],
      },
     
    ];
    
    }



msgConfirmacionLogout=()=>{
    Swal.fire({
      title: "Cerrar Sesión",
      text: "¿Está seguro de que desea cerrar sesión?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Cerrar Sesión",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
          title: "Session cerrada",
          text: "Ha salido existosamente de su cuenta",
          icon: "success"
        });
        this.logout();
      }
    });
  }
  }

