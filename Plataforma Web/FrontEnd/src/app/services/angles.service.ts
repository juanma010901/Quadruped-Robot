import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AnglesService {

  urlApiTG = 'http://localhost:7175/api'
  // urlApiTG = "https://masterusers.azurewebsites.net/api";
  // urlApiTG = "https://tg-backend-jl.azurewebsites.net/api";

  constructor(private http: HttpClient) { }

  public GetAngles(): Observable<any> {
    const url = `${this.urlApiTG}/GetAngulos`;
    return this.http.get(url);
  }
}
