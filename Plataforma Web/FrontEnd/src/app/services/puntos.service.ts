import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { PuntosModel } from '../models/PuntosModel';

@Injectable({
  providedIn: 'root'
})

export class PuntosService {

  urlApiTG = 'http://localhost:7175/api';
  // urlApiTG = "https://tg-backend-jl.azurewebsites.net/api";
  // urlApiTG = "https://masterusers.azurewebsites.net/api";

  constructor(private http: HttpClient) { }

  public ActualizarPunto(request: PuntosModel): Observable<any> {
    const url = `${this.urlApiTG}/ActualizarPunto`;
    return this.http.put(url, request);
  }

  
  public GetPuntosById(puntoId: number): Observable<any> {
    const url = `${this.urlApiTG}/GetPuntosById/${puntoId}`;
    return this.http.get(url);
  }
}
