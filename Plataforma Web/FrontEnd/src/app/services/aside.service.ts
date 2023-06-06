import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AsideService {

  private closeAsideSubject: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  public closeAside$ = this.closeAsideSubject.asObservable();

  toggleCloseAside(value: boolean): void {
    this.closeAsideSubject.next(value);
  }
}
