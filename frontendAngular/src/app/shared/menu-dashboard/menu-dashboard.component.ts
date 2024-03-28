import { Component,ViewChild } from '@angular/core';
import { MenuItem } from 'primeng/api';
import { AuthService } from '../../services/auth.service';
import Swal from 'sweetalert2'
import { Router } from '@angular/router';
import { SidebarComponent } from '../sidebar/sidebar.component';


@Component({
  selector: 'app-menu-dashboard',
  templateUrl: './menu-dashboard.component.html',
  styleUrl: './menu-dashboard.component.css'
})
export class MenuDashboardComponent {
  @ViewChild(SidebarComponent) sidebar!: SidebarComponent;

  elem_izq: MenuItem[] =[];
  sidebarVisible: boolean = false;
  
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
    this.elem_izq = [
      {
        icon: 'pi pi-fw pi-bars',
        command: () => this.toggleSidebar()
        

      
      },

    ];
    
    }

    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible;
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

