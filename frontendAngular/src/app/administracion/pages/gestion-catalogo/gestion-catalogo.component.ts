import { Component , OnInit } from '@angular/core';
import { LibrosService } from '../../../services/libros.service';
import { ActivatedRoute, Router } from '@angular/router';
import Swal from 'sweetalert2';


@Component({
  selector: 'app-gestion-catalogo',
  templateUrl: './gestion-catalogo.component.html',
  styleUrl: './gestion-catalogo.component.css'
})
export class GestionCatalogoComponent implements OnInit{

  libros: any[] =[]; 
  totalRecords: number=0;
  busqueda: string = '';

  constructor(private LibrosService: LibrosService, private Router:Router, private activatedRouter: ActivatedRoute ) { }

  ngOnInit() {
    this.obtenerLibros();
    this.activatedRouter.queryParams.subscribe(params => {
      this.busqueda = params['q'] || '';
      this.cargaLibroBusqueda();
    });
  }

  obtenerLibros() {
    this.LibrosService.listarLibros().subscribe(
      (data) => {
        this.libros = data;
        this.totalRecords = data.length;
      },
      (error) => {
        console.error(error);
      }
    );
  }

  cargaLibroBusqueda(): void {
    if (this.busqueda === '') {
      this.obtenerLibros();
      return;
    }
    this.LibrosService.buscarLibro(this.busqueda).subscribe({
      next: (data) => {
        this.libros = data;
      },
      error: (error) => {
        console.error('Error al obtener los libros', error);
      },
      complete: () => {
        console.log('Carga de libros completada');
      }
    });
  }

  eliminar(id: number) {
    Swal.fire({
      title: "¿Está seguro de realizar esta operación?",
      text: "Esta  acción no se puede deshacer",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Eliminar",
      cancelButtonText: "Cancelar"
    }).then((result) => {
      if (result.isConfirmed) {
        this.LibrosService.borrarLibro(id).subscribe(
          () => {
            Swal.fire({
              title: "Libro eliminaado con éxito",
              icon: "success"
            });
            this.obtenerLibros();
          },
          (error) => {
            Swal.fire({
              title: "Error!",
              text: "Ha ocurrido un error al intentar eliminar el libro.",
              icon: "error"
            });
          }
        );
      }
      else {
        Swal.fire({
          title: "Operación cancelada",
          icon: "error"
        });
      }
    });
  }

  editar(id: number) {
    
  }

  masinfo(id: number) {
    this.Router.navigate(['/info_libro', id]);
  }


}
