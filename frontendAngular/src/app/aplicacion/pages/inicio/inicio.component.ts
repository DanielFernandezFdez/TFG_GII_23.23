import { Component,OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { LibrosService } from '../../../services/libros.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-inicio',
  templateUrl: './inicio.component.html',
  styleUrl: './inicio.component.css'
})
export class InicioComponent implements OnInit{
  countries: any[] | undefined;
  busqueda: string = '';
  formGroup: FormGroup | undefined;

  filteredCountries: any[] | undefined;

  constructor(private librosService: LibrosService, private router: Router) { }

  ngOnInit() {
  
  }

  buscarCatalogo() {
    console.log(this.busqueda);
    this.router.navigate(['/catalogo'],{ queryParams: { q: this.busqueda } });
    }
  


}
