import { Component } from '@angular/core';

@Component({
  selector: 'app-referentes',
  templateUrl: './referentes.component.html',
  styleUrl: './referentes.component.css'
})
export class ReferentesComponent {
  investigaciones = [
    {
      titulo: "Ejemplo 1",
      descripcion: "Descripción 1",
      url: "https://ejemplo.com/investigacion1"
    },
    {
      titulo: "Ejemplo 2",
      descripcion: "Descripción 2",
      url: "https://ejemplo.com/investigacion2"
    }
 
  ];
}
