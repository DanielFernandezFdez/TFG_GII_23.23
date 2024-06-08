import { Component, OnInit } from '@angular/core';
import { LibrosService } from '../../../services/libros.service';
import { FormGroup, FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-panel-admin',
  templateUrl: './panel-admin.component.html',
  styleUrls: ['./panel-admin.component.css']
})
export class PanelAdminComponent implements OnInit {
  estadisticas: any[] = [];
  barData: any;
  lineData: any;
  userData: any;
  libroMasVisitado : any
  rangoForm: FormGroup = this.fb.group({
    rangoFechas: [null]
  });
  maxDateValue: Date = new Date(); 
  es: any;

  constructor(private librosService: LibrosService, private fb: FormBuilder) {}

  ngOnInit(): void {
    this.es = {
      firstDayOfWeek: 1,
      dayNames: ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
      dayNamesShort: ["dom", "lun", "mar", "mié", "jue", "vie", "sáb"],
      dayNamesMin: ["D", "L", "M", "X", "J", "V", "S"],
      monthNames: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
      monthNamesShort: ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"],
      today: 'Hoy',
      clear: 'Limpiar',
      dateFormat: 'dd/mm/yy'
    };
    this.cargarEstadisticas();
    this.rangoForm = this.fb.group({
      rangoFechas: [null]
    });


    this.maxDateValue = new Date();
  }

  cargarEstadisticas(): void {
    this.librosService.obtenerEstadisticas().subscribe(data => {
      this.estadisticas = data;
      console.log(this.estadisticas)
      this.configurarDatos();
      this.libroMasVisitado = this.estadisticas.reduce((max, libro) => libro.visitas_libro_mas_visitado > max.visitas_libro_mas_visitado ? libro : max);
    });
  }

  configurarDatos(): void {
    const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    this.barData = {
      labels: this.estadisticas.map(est => meses[est.mes - 1]),
      datasets: [
        {
          label: 'Visitas Totales',
          backgroundColor: '#42A5F5',
          data: this.estadisticas.map(est => est.numero_visitas_totales)
        },
        {
          label: 'Visitas del Libro Más Visitado',
          backgroundColor: '#FFA726',
          data: this.estadisticas.map(est => est.visitas_libro_mas_visitado)
        }
      ]
    };

    this.lineData = {
      labels: this.estadisticas.map(est => meses[est.mes - 1]),
      datasets: [
        {
          label: 'Número de Sugerencias',
          borderColor: '#66BB6A',
          data: this.estadisticas.map(est => est.numero_sugerencias),
          fill: false
        },
        {
          label: 'Número de Estimaciones',
          borderColor: '#FFA726',
          data: this.estadisticas.map(est => est.numero_estimaciones),
          fill: false
        },
        {
          label: 'Número de Libros',
          borderColor: '#33BEFF',
          data: this.estadisticas.map(est => est.numero_libros),
          fill: false
        }
      ]
    };
    this.userData = {
      labels: this.estadisticas.map(est => meses[est.mes - 1]),
      datasets: [{
        label: 'Número de Usuarios',
        backgroundColor: '#42A5F5',
        data: this.estadisticas.map(est => est.numero_usuarios)
      }]
    };
  }


    cargarEstadisticasFiltradas(): void {
      if (this.rangoForm.value.rangoFechas) {
        const { rangoFechas } = this.rangoForm.value;
        const mesInicio = rangoFechas[0].getMonth() + 1;
        console.log(mesInicio)
        const anyoInicio = rangoFechas[0].getFullYear();
        console.log(anyoInicio)
        const mesFin = rangoFechas[1].getMonth() + 1;
        console.log(mesFin)
        const anyoFin = rangoFechas[1].getFullYear();
        console.log(anyoFin)

        const fechaInicio = new Date(anyoInicio, mesInicio - 1);
        const fechaFin = new Date(anyoFin, mesFin - 1);
        const diffTime = Math.abs(fechaFin.getTime() - fechaInicio.getTime());
        const diffMonths = Math.ceil(diffTime / (1000 * 60 * 60 * 24 * 30));
        console.log(diffMonths)
        if (diffMonths > 12) {
          alert('El rango no puede exceder los 12 meses.');
          return;
        }
  
        this.librosService.obtenerEstadisticasFiltradas(mesInicio, anyoInicio, mesFin, anyoFin).subscribe(data => {
          this.estadisticas = data;
      this.configurarDatos();
      this.libroMasVisitado = null
      this.libroMasVisitado = this.estadisticas.reduce((max, libro) => libro.visitas_libro_mas_visitado > max.visitas_libro_mas_visitado ? libro : max);
        });
      }
    }
}
