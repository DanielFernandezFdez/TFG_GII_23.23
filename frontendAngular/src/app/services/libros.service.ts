import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LibrosService {
  private apiUrl = 'http://127.0.0.1:5000'; 
  private apiKey = 'clave'; 
  constructor(private http: HttpClient) { }

  private getHeaders() {
    return new HttpHeaders().set("X_API_KEY", this.apiKey);
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

  agregarLibro(libro: any, borrador: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/agregar_libro/${borrador}`, libro, { headers: this.getHeaders() });
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

}