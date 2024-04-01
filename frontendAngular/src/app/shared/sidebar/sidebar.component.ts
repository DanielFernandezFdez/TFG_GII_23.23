import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';
import { LibrosService } from '../../services/libros.service';



@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent {
  items: any[];
  archivoSeleccionado!: File;
  @Input() visible: boolean = false;
  @Output() visibleChange = new EventEmitter<boolean>();
  
  constructor(private router: Router, private LibrosService:LibrosService) {
    this.items = [
      {
        label: 'Pantallas Generales',
        expanded: true,
        items: [
          { 
            label: 'Inicio', 
            icon: 'pi pi-home',
            command: () =>  {
              this.router.navigate(['/']),
             this.cerrarSidebar() }
          },
          { 
            label: 'Catálogo', 
            icon: 'pi pi-list',
            command: () =>  {
              this.router.navigate(['/catalogo']),
             this.cerrarSidebar() }  
          },
          {
            label: 'Guía de análisis',
            icon: 'pi pi-fw pi-info-circle',
            command: () =>  {
              this.router.navigate(['/']),
             this.cerrarSidebar() }
            
          },
          {
            label: 'Decálogo',
            icon: 'pi pi-bars',
            command: () =>  {
              this.router.navigate(['/']),
             this.cerrarSidebar() }
           
          },
          {
            label: 'Referentes',
            icon: 'pi pi-bookmark-fill',
            command: () =>  {
              this.router.navigate(['/']),
             this.cerrarSidebar() }
      
          },
          {
            label: 'Guía de puntuación',
            icon: 'pi pi-fw pi-info-circle',
            command: () =>  {
              this.router.navigate(['/']),
             this.cerrarSidebar() }
      
          },
          {
            label: 'Valoración',
            icon: 'pi pi-fw pi-calculator',
            command: () =>  {
              this.router.navigate(['/estimador']),
             this.cerrarSidebar() }
      
          }
        ]
      },
      {
        label: 'Gestión de usuarios',
        expanded: true,
        items: [
          {
            label: 'Gestión de usuarios',
            icon: 'pi pi-user-edit',
            command: () =>  {
              this.router.navigate(['/']),
             this.cerrarSidebar() }
          },
          {
            label: 'Gestión de roles',
            icon: 'pi pi-eye-slash',
            command: () =>  {
              this.router.navigate(['/']),
             this.cerrarSidebar() }
          }
        ]
      },
      {
        label: 'Gestión de catálogo',
        expanded: true,
        items: [
          {
            label: 'Agregar Libro manual',
            icon: 'pi pi-plus',
            command: () =>  {
              this.router.navigate(['/agregar']),
             this.cerrarSidebar() }
            
          },
          {
            label: 'Agregar Libro auto',
            icon: 'pi pi-send',
            command: () =>{
              this.obtenerNombreLibroAuto(), 
              this.cerrarSidebar()
            } 
          },
          {
            label: 'Gestionar Catálogo',
            icon: 'pi pi-book',
            command: () => 
            {
              this.router.navigate(['/gestion-catalogo']),
              this.cerrarSidebar()
            }
          },
          {
            label: 'Importación y exportación',
            icon: 'pi pi-upload',
            items: [
              {
                label: 'Importar',
                icon: 'pi pi-download',
                command: () => {
                  this.decisionExportacion(),
                  this.cerrarSidebar(),
                  this.router.navigate(['/gestion-catalogo'])
                }
              },
              {
                label: 'Exportar',
                icon: 'pi pi-upload',
                command: () => {
                  this.exportarLibros(), 
                  this.cerrarSidebar()
                  
                }
              }
            ]
          }
        ]
      }
    ];
  };
   
  cerrarSidebar() {
    this.visible = false;
    this.visibleChange.emit(this.visible);
  };

  obtenerNombreLibroAuto() {
    Swal.fire({
      title: 'Introduce el nombre del libro',
      input: 'text',
      inputAttributes: {
        autocapitalize: 'off'
      },
      showCancelButton: true,
      confirmButtonText: 'Aceptar',
      cancelButtonText: 'Cancelar',
      showLoaderOnConfirm: true,
      preConfirm: (nombre) => {
        return nombre;
      },
      allowOutsideClick: () => !Swal.isLoading()
    }).then((result) => {
      if (result.isConfirmed) {
        this.router.navigate(['/agregar_auto', result.value]);
      }
    });
  }




  exportarLibros() {
    this.LibrosService.exportarLibros().subscribe((res) => {
      // Crear un objeto Blob con los datos recibidos
      const blob = new Blob([res], { type: 'text/csv' });
  
      // Crear una URL para el Blob
      const url = window.URL.createObjectURL(blob);
  
      // Crear un elemento <a> temporal para realizar la descarga
      const a = document.createElement('a');
      a.href = url;
      a.download = 'libros.csv';  // Nombre del archivo a descargar
      document.body.appendChild(a);  // Agregar el elemento al DOM
      a.click();  // Iniciar la descarga
  
      // Limpiar y remover el elemento <a>
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    });
  }

  abrirDialogoArchivo(): void {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.csv';
    input.onchange = (event: any) => {
      this.archivoSeleccionado = event.target.files[0];
      if (this.archivoSeleccionado) {
        this.importarLibros();
      }
    };
    input.click();
  }

  importarLibros(): void {
    if (this.archivoSeleccionado) {
      this.LibrosService.importarLibros(this.archivoSeleccionado).subscribe({
        next: (res) => 
        Swal.fire({
          title: "Importación completada",
          text: "Los libros se han importado correctamente",
          icon: "success"
        }),
        error: (err) => 
        Swal.fire({
          title: "Error",
          text: "Ha ocurrido un error al importar los libros",
          icon: "error"
        })
      });
    }
  }
  

  decisionExportacion():void {
    Swal.fire({
      title: "Es recomendable exportar los libros antes de importar nuevos",
      text: "Esta acción sobreescribirá los libros actuales ¿Desea continuar?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Importar",
      cancelButtonText: "Cancelar"
    }).then((result) => {
      if (result.isConfirmed) {
        this.abrirDialogoArchivo();
      }

    });
  }
}