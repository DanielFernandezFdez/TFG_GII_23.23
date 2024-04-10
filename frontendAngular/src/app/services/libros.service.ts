import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LibrosService {
  private apiUrl = 'http://127.0.0.1:5000'; 

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
    return this.http.get(`${this.apiUrl}/libros`, { headers: this.getHeaders() });
  }

  buscarLibro(busqueda: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/busqueda/${busqueda}`, { headers: this.getHeaders() });
  }

  obtenerInfoLibro(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/infoLibro/${id}`, { headers: this.getHeaders() });
  }

  agregarLibro(libro: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/agregar_libro`, libro, { headers: this.getHeaders() });
  }

  editarLibro(id: number, libro: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/editarLibro/${id}`, libro, { headers: this.getHeaders() });
  }

  borrarLibro(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/borrarLibro/${id}`, { headers: this.getHeaders() });
  }
  
  fecha(): Observable<any> {
    return this.http.get(`${this.apiUrl}/fecha`, { headers: this.getHeaders() });
  }

  
  buscarLibroAutomatico(elemento: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/buscar_libro_automatico`, { elemento }, { headers: this.getHeaders() });
  }

  listarLibrosAutomaticos(): Observable<any> {
    return this.http.get(`${this.apiUrl}/listar_libros_automaticos`, { headers: this.getHeaders() });
  }

  borrarTablaLibrosAutomaticos(): Observable<any> {
    return this.http.delete(`${this.apiUrl}/borrar`, { headers: this.getHeaders() });
  }

  exportarLibros(): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/exportar_csv`, {
      headers: this.getHeaders(),
      responseType: 'blob'
    });
  }

  importarLibros(archivo: File): Observable<any> {
    const formData: FormData = new FormData();
    formData.append('archivo', archivo, archivo.name);
  
    const headers = this.getHeaders();
  
    return this.http.post(`${this.apiUrl}/importar_csv`, formData, { headers });
  }


}
