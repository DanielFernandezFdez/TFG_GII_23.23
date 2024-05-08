import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EstimacionService {
  private apiUrl = 'https://tfg-gii-23-23.onrender.com'; 
  constructor(private http: HttpClient) { }

  private getHeaders() {
    let headers = new HttpHeaders();
    const token = localStorage.getItem('token'); 
    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }
    return headers;
  }

  obtenerListados(): Observable<any> {
    return this.http.get(`${this.apiUrl}/gestion-estimacion/obtenerListados`, { headers: this.getHeaders() });
  }

  GenerarListados(listados: any,): Observable<any> {
    return this.http.post(`${this.apiUrl}/gestion-estimacion/generarListados`, listados, { headers: this.getHeaders() });
  }

  guardarEstimacion(estimacion: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/gestion-estimacion/guardarEstimacion`, estimacion, { headers: this.getHeaders() });
  }

  borrarListados(): Observable<any> {
    return this.http.delete(`${this.apiUrl}/gestion-estimacion/borrarListados`, { headers: this.getHeaders() });
  }
  
  calcularEstimacion(valoresEstimacion: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/gestion-estimacion/calcularEstimacion`,  valoresEstimacion , { headers: this.getHeaders() });
  }

  listarEstimaciones(): Observable<any> {
    return this.http.get(`${this.apiUrl}/gestion-estimacion/listarEstimaciones`, { headers: this.getHeaders() });
  }

  borrarEstimacion(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/gestion-estimacion/borrarEstimacion/${id}`, { headers: this.getHeaders() });
  }





}