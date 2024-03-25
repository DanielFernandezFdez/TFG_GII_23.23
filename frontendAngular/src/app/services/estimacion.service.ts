import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EstimacionService {
  private apiUrl = 'http://127.0.0.1:5000'; 
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
    return this.http.get(`${this.apiUrl}/obtenerListados`, { headers: this.getHeaders() });
  }

  GenerarListados(listados: any,): Observable<any> {
    return this.http.post(`${this.apiUrl}/generarListados`, listados, { headers: this.getHeaders() });
  }


  borrarListados(): Observable<any> {
    return this.http.delete(`${this.apiUrl}/borrarListados`, { headers: this.getHeaders() });
  }
  
  calcularEstimacion(valoresEstimacion: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/estimacion`,  valoresEstimacion , { headers: this.getHeaders() });
  }





}