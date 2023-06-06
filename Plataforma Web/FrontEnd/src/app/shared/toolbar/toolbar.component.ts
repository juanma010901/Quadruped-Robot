import { Component, EventEmitter, Output } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, Subscription, fromEvent, map } from 'rxjs';

@Component({
  selector: 'app-toolbar',
  templateUrl: './toolbar.component.html'
})
export class ToolbarComponent {
  
  observerWidth: Observable<number>;
  subscriptionWidth: Subscription;
  showOptions: boolean = false;
  @Output() onOpenEvent: EventEmitter<void>;

  constructor(private router: Router) {
    this.onOpenEvent = new EventEmitter<void>();
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
    })
  }

  onOpenClick() {
    this.onOpenEvent.emit();
  }

  private getWindowWidth(data: number) {
    if (data <= 767.98) {
      this.showOptions = true;
    } else {
      this.showOptions = false;
    }
  }

  ngOnDestroy(): void {
    if (this.subscriptionWidth) {
      this.subscriptionWidth.unsubscribe();
    }
  }

  logOut() {
    this.router.navigate(['login']);
  }

}
