import { Injectable } from '@angular/core';
import { ModosModel } from '../models/ModosModel';
import { Observable } from 'rxjs';
import { HttpClient, HttpStatusCode } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ModosService {

  urlApiTG = 'http://localhost:7175/api'
  // urlApiTG = "https://masterusers.azurewebsites.net/api";
  // urlApiTG = "https://tg-backend-jl.azurewebsites.net/api";

  constructor(private http: HttpClient) { }


  public ActualizarModo(request: ModosModel): Observable<any> {
    const url = `${this.urlApiTG}/ActualizarModo`;
    return this.http.put(url, request);
  }

  public GetModoActual(): Observable<any> {
    const url = `${this.urlApiTG}/GetModoActual`;
    return this.http.get(url);
  }

  public GetModos(): Observable<any> {
    const url = `${this.urlApiTG}/GetModos`;
    return this.http.get(url);
  }

}
