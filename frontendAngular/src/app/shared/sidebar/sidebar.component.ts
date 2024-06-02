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
              this.router.navigate(['/guia-analisis']),
             this.cerrarSidebar() }
            
          },
          {
            label: 'Decálogo',
            icon: 'pi pi-bars',
            command: () =>  {
              this.router.navigate(['/decalogo']),
             this.cerrarSidebar() }
           
          },
          {
            label: 'Referentes',
            icon: 'pi pi-bookmark-fill',
            command: () =>  {
              this.router.navigate(['/referentes']),
             this.cerrarSidebar() }
      
          },
          {
            label: 'Valoración',
            icon: 'pi pi-fw pi-calculator',
            command: () =>  {
              this.router.navigate(['/estimador']),
             this.cerrarSidebar() }
      
          },
          {
            label: 'Información',
            icon: 'pi pi-star-fill',
            routerLink: ['/colaboradores'],
          },
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
              this.router.navigate(['/gestion-usuarios']),
             this.cerrarSidebar() }
          },
          {
            label: 'Gestión de roles',
            icon: 'pi pi-eye-slash',
            command: () =>  {
              this.router.navigate(['/gestion-roles']),
             this.cerrarSidebar() }
          },
          {
            label: 'Gestión de colaboradores',
            icon: 'pi pi-users',
            command: () =>  {
              this.router.navigate(['/gestion-colaboradores']),
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
            label: 'Agregar Libro automáticamente',
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
                  this.decisionExtensionExportacion(), 
                  this.cerrarSidebar()
                  
                }
              }
            ]
          }
        ]
      },
      {
        label: 'Gestión de las valoraciones',
        expanded: true,
        items: [
          {
            label: 'Gestión de actividades',
            icon: 'pi pi-sitemap',
            command: () =>  {
              this.router.navigate(['/gestion-estimador']),
             this.cerrarSidebar() }
          },
          {
            label: "Valoraciones guardadas",
            icon: 'pi pi-save',
            command: () =>  {
              this.router.navigate(['/estimaciones-guardadas']),
             this.cerrarSidebar() }
          }
         
        ]
      },
    ];
  };
   
  cerrarSidebar() {
    this.visible = false;
    this.visibleChange.emit(this.visible);
  };

  obtenerNombreLibroAuto() {
    Swal.fire({
      title: 'Introduce el nombre o ISBN del libro',
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


  decisionExtensionExportacion():void {
    Swal.fire({
      title: "¿Qué formato desea exportar?",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Excel",
      cancelButtonText: "CSV"
    }).then((result) => {
      if (result.isConfirmed) {
        this.LibrosService.exportarLibrosEXCEL().subscribe((res) => {
          const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'libros.xlsx';
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          document.body.removeChild(a);
        });
      } else if (result.dismiss === Swal.DismissReason.cancel) {
        this.LibrosService.exportarLibrosCSV().subscribe((res) => {
          const blob = new Blob([res], { type: 'text/csv' });
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'libros.csv'; 
          document.body.appendChild(a);  
          a.click(); 
          window.URL.revokeObjectURL(url);
          document.body.removeChild(a);
        });
      }
    });
  }


  abrirDialogoArchivo(): void {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.xlsx, .csv';
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