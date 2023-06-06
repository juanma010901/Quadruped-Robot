import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LoginComponent } from './pages/login/login.component';
import { AngularMaterialModule } from './angular-material.module';
import { AsideComponent } from './shared/aside/aside.component';
import { HomeComponent } from './pages/home/home.component';
import { ToolbarComponent } from './shared/toolbar/toolbar.component';
import { InformationComponent } from './pages/home/information/information.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CentroControlComponent } from './pages/centro-control/centro-control.component';
import { ToastrModule } from 'ngx-toastr';
import { NgxSpinnerModule } from 'ngx-spinner';
import { ChartCustomComponent } from './shared/chart-custom/chart-custom.component';
import { NgChartsModule } from 'ng2-charts';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    AsideComponent,
    HomeComponent,
    ToolbarComponent,
    InformationComponent,
    CentroControlComponent,
    ChartCustomComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    ToastrModule.forRoot(),
    AngularMaterialModule, 
    FormsModule,
    ReactiveFormsModule,
    NgxSpinnerModule,
    NgChartsModule
  ],
  exports:[
    LoginComponent,
    AsideComponent,
    HomeComponent,
    ToolbarComponent,
    InformationComponent,
    CentroControlComponent,
    ChartCustomComponent
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
