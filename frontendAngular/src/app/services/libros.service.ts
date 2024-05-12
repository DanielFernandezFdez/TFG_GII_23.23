import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LibrosService {
  //private apiUrl = 'http://127.0.0.1:5000';
  private apiUrl = 'https://tfg-gii-23-23.onrender.com'; 

  private libroInfoConexion = new BehaviorSubject<any>(null);
  libroInfo = this.libroInfoConexion.asObservable();

  constructor(private http: HttpClient) { }

  private getHeaders() {
    let headers = new HttpHeaders();
    const token = localStorage.getItem('token');
    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }
    return headers;
  }

  conexionLibroInfo(libro: any) {
    this.libroInfoConexion.next(libro);
  }

  listarLibros(): Observable<any> {
    return this.http.get(`${this.apiUrl}/gestion-libros/listadoLibros`, { headers: this.getHeaders() });
  }

  buscarLibro(busqueda: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/gestion-libros/busquedaLibro/${busqueda}`, { headers: this.getHeaders() });
  }

  obtenerInfoLibro(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/gestion-libros/infoLibro/${id}`, { headers: this.getHeaders() });
  }

  agregarLibro(libro: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/gestion-libros/agregarLibro`, libro, { headers: this.getHeaders() });
  }

  editarLibro(id: number, libro: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/gestion-libros/editarLibro/${id}`, libro, { headers: this.getHeaders() });
  }

  borrarLibro(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/gestion-libros/borrarLibro/${id}`, { headers: this.getHeaders() });
  }
  
  fecha(): Observable<any> {
    return this.http.get(`${this.apiUrl}/gestion-libros/fecha`, { headers: this.getHeaders() });
  }

  
  buscarLibroAutomatico(elemento: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/gestion-libros/buscarLibroAutomatico`, { elemento }, { headers: this.getHeaders() });
  }

  listarLibrosAutomaticos(): Observable<any> {
    return this.http.get(`${this.apiUrl}/gestion-libros/listarLibrosAutomaticos`, { headers: this.getHeaders() });
  }


  exportarLibrosCSV(): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/import-export/exportar_csv`, {
      headers: this.getHeaders(),
      responseType: 'blob'
    });
  }

  exportarLibrosEXCEL(): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/import-export/exportar_excel`, {
      headers: this.getHeaders(),
      responseType: 'blob'
    });
  }

  importarLibros(archivo: File): Observable<any> {
    const formData: FormData = new FormData();
    formData.append('archivo', archivo, archivo.name);
  
    const headers = this.getHeaders();
  
    return this.http.post(`${this.apiUrl}/import-export/importar_archivo`, formData, { headers });
  }


  obtenerEstadisticas(): Observable<any> {
    return this.http.post(`${this.apiUrl}/gestion-estimacion/obtenerEstadisticasGraficosGenerales`, {},{headers: this.getHeaders()});
  }

  obtenerEstadisticasFiltradas(mesInicio: number, anyoInicio: number, mesFin: number, anyoFin: number): Observable<any> {
    const filtro = { mes_inicio: mesInicio, anyo_inicio: anyoInicio, mes_fin: mesFin, anyo_fin: anyoFin };
    return this.http.post(`${this.apiUrl}/gestion-estimacion/obtenerEstadisticasGraficosGenerales`, filtro, { headers: this.getHeaders() });
  }


}
