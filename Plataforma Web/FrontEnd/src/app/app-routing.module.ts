import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { HomeComponent } from './pages/home/home.component';
import { InformationComponent } from './pages/home/information/information.component';
import { CentroControlComponent } from './pages/centro-control/centro-control.component';
import { AnglesComponent } from './pages/angles/angles.component';
import { ElectricalComponent } from './pages/electrical/electrical.component';
import { ObstaclesComponent } from './pages/obstacles/obstacles.component';

const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: "login", component: LoginComponent },
  { 
    path: "main", component: HomeComponent ,
    children:[{
      path:'information',
      component:InformationComponent,
      data:{
          parent:'main',
          title:'Pagos'
      }
    },
    {
      path:'control',
      component:CentroControlComponent,
      data:{
          parent:'main',
          title:'Pagos'
      }
    },
    {
      path:'angles',
      component:AnglesComponent,
      data:{
          parent:'main',
          title:'Pagos'
      }
    },
    {
      path:'electrical',
      component:ElectricalComponent,
      data:{
          parent:'main',
          title:'Pagos'
      }
    }
    ,
    {
      path:'obstacles',
      component:ObstaclesComponent,
      data:{
          parent:'main',
          title:'Pagos'
      }
    }
  ]
  },

  { path: '**', redirectTo: 'login', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
