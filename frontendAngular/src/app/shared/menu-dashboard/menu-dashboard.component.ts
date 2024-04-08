import { Component,OnInit, ViewChild } from '@angular/core';
import { MenuItem } from 'primeng/api';
import { AuthService } from '../../services/auth.service';
import Swal from 'sweetalert2'
import { Router } from '@angular/router';
import { SidebarComponent } from '../sidebar/sidebar.component';
import { LibrosService } from '../../services/libros.service';


@Component({
  selector: 'app-menu-dashboard',
  templateUrl: './menu-dashboard.component.html',
  styleUrl: './menu-dashboard.component.css'
})
export class MenuDashboardComponent implements OnInit{
  @ViewChild(SidebarComponent) sidebar!: SidebarComponent;

  elem_izq: MenuItem[] =[];
  sidebarVisible: boolean = false;
  
  libros_resultado: any[] = [];
  termino: string = '';
  
  constructor(public authService: AuthService, public libroService :LibrosService, private router: Router) {
    }
  items: any[]=[];
  
  logout() {
    this.authService.logout();
  }
  ngOnInit() {            
    this.elem_izq = [
      {
        icon: 'pi pi-bars',
        command: () => this.toggleSidebar()
      }
    ];
    this.items = [
      {
        label: 'Panel de Administrador',
        icon: 'pi pi-cog',
        command: () => {
          this.router.navigate(['/panel-admin'])
        }
      },
      {
        label: 'Cambiar contraseña',
        icon: 'pi pi-shield',
        command: () => {
          this.router.navigate(['/panel-admin'])
        }
      },
      {
        label: 'Cerrar Sesión',
        icon: 'pi pi-sign-out ',
        command: () => this.msgConfirmacionLogout()}];
    
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


  busqueda(event: any) {
    const query = event.query;
    this.libroService.buscarLibro(query).subscribe(data => {
      this.libros_resultado = data.map((libro: any) => ({
        titulo: libro.titulo, 
        isbn: libro.isbn,  
        id: libro.id
      }));
    });
  }

  libroSeleccionado(event: any) {
    const idLibro = event.value.id;
    this.router.navigate(['/info_libro', idLibro]);
  }
}


