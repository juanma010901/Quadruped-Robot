import { Component } from '@angular/core';
import { MatDrawerMode } from '@angular/material/sidenav';
import { Observable, Subscription, fromEvent, map } from 'rxjs';
import { AsideService } from 'src/app/services/aside.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
})
export class HomeComponent {
  
  drawerMode: MatDrawerMode;
  isDraweOpened: boolean = true;
  observerWidth: Observable<number>;
  subscriptionWidth: Subscription;
  closeAsideSubscription: Subscription;
  closeAside: boolean;

  constructor(private asideService: AsideService) {
    this.drawerMode = 'side';
  }

  ngOnInit(): void {
    this.getWindowWidth(window.innerWidth);

    this.observerWidth = fromEvent(window, 'resize').pipe(
      map(() => {
        return window.innerWidth;
      })
    );

    this.subscriptionWidth = this.observerWidth.subscribe({
      next: (data) => {
        this.getWindowWidth(data);
      }
    });


  }

  ngOnDestroy() {
    this.closeAsideSubscription.unsubscribe();
  }


  private getWindowWidth(data: number) {
    if (data <= 767.98) {
      this.drawerMode = 'over';
      this.isDraweOpened = false;

      this.closeAsideSubscription = this.asideService.closeAside$.subscribe((value) => {
        if(value){
          this.isDraweOpened  = false;
          this.asideService.toggleCloseAside(false);
        }
      });

    } else {
      this.drawerMode = 'side';
      this.isDraweOpened = true;
    }
  }

  onOpenClick() {
    this.isDraweOpened = true;
  }

  onClose() {
    this.isDraweOpened = window.innerWidth <= 767.98 ? false : true;
  }

}
