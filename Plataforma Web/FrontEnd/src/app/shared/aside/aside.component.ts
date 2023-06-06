import { Component } from '@angular/core';
import { AsideService } from 'src/app/services/aside.service';

@Component({
  selector: 'app-aside',
  templateUrl: './aside.component.html'
})
export class AsideComponent {

  openAside: boolean = true;  

  constructor(private asideService: AsideService) {}


  onClose(){
    this.openAside = true;
    this.asideService.toggleCloseAside(this.openAside);
    console.log("en shared:_ ",this.openAside)
  }

}
