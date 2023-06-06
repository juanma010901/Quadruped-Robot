import { Component, OnInit } from '@angular/core';
import { Observable, forkJoin } from 'rxjs';
import { ModosModel } from 'src/app/models/ModosModel';
import { ModosService } from 'src/app/services/modos.service';
import { ToastrService } from 'ngx-toastr';
import { FormBuilder, FormGroup } from '@angular/forms';
import { PuntosModel } from 'src/app/models/PuntosModel';
import { PuntosService } from 'src/app/services/puntos.service';
import { NgxSpinnerService } from 'ngx-spinner';
import { AnglesService } from 'src/app/services/angles.service';
import { ChartDataCustom } from 'src/app/models/ChartDataCustom';

@Component({
  selector: 'app-centro-control',
  templateUrl: './centro-control.component.html',
})

export class CentroControlComponent implements OnInit {

  isChecked: boolean = false; 
  operationMode: string = 'Puntos';
  PuntosDefinidos: ModosModel[];
  MarchasDefinidas: ModosModel[];

  puntosHome: PuntosModel;

  patasForm: FormGroup;

  intervalId: any;
  modoIdAnterior: number = 0;
  modoIdActual: number = 0;

  secionIdActiva: number = 0;

  puntosHomeAjuste: number[] = [0,13]

  dataChartSelected: ChartDataCustom = {};

  angulo11: number[] = [];
  angulo12: number[] = [];
  angulo21: number[] = [];
  angulo22: number[] = [];
  angulo31: number[] = [];
  angulo32: number[] = [];
  angulo41: number[] = [];
  angulo42: number[] = [];

  hora: string[] = [];

  pataSelected: string = 'pata1';
  titlePataSelected: string = 'Pata 1';



  constructor(private fb: FormBuilder,
    private modosService: ModosService,
    private puntosService: PuntosService,
    private anglesService: AnglesService,
    private toastr: ToastrService,
    private spinner: NgxSpinnerService
    ) {}

  ngOnInit(): void {
    
    this.loadData();
    this.initFilterForm();

    this.intervalId = setInterval(() => {
      this.getMode();
    }, 500);
  }

  initFilterForm() {
    this.patasForm = this.fb.group({
      P1X: [null],
      P1Y: [null],
      P2X: [null],
      P2Y: [null],
      P3X: [null],
      P3Y: [null],
      P4X: [null],
      P4Y: [null],
    });
  }

  getMode(){
    this.modosService.GetModoActual().subscribe({
      next: response => {
        this.modoIdActual = response.id;

        if(this.modoIdActual !== this.modoIdAnterior){
          this.loadData();
        }
      },
      error: err => {

      }
    })

    this.anglesService.GetAngles().subscribe({
      next: response => {

      if(this.angulo11.length !== response.length){
        
        this.angulo11 = [];
        this.angulo12 = [];
        this.hora = [];
        response.forEach(obj => {
          this.angulo11.push(obj.a11);
          this.angulo12.push(obj.a12);
          this.angulo21.push(obj.a21);
          this.angulo22.push(obj.a22);
          this.angulo31.push(obj.a31);
          this.angulo32.push(obj.a32);
          this.angulo41.push(obj.a41);
          this.angulo42.push(obj.a42);
          this.hora.push(obj.fecha);
        })

        this.hora = this.hora.map(hora => {
          const dia = hora.slice(11, 16);
          return dia;
        });

      }

      let _dataChartSelected: ChartDataCustom;
      this.dataChartSelected = {};

      switch (this.pataSelected) {

        

        case 'pata1':
          this.titlePataSelected = 'Pata 1';
          _dataChartSelected = this.setChart(this.angulo11,this.angulo12,this.hora,'Hora','Grados','Motor 1','Motor 2','#0C00FF','#FF0909')
          this.dataChartSelected.dataChartOptions =  _dataChartSelected.dataChartOptions;
          this.dataChartSelected.lineChartOptions =  _dataChartSelected.lineChartOptions;
          
          break;
      
        case 'pata2':
          this.titlePataSelected = 'Pata 2';
          _dataChartSelected = this.setChart(this.angulo21,this.angulo22,this.hora,'Hora','Grados','Motor 1','Motor 2','#0C00FF','#FF0909')
          this.dataChartSelected.dataChartOptions =  _dataChartSelected.dataChartOptions;
          this.dataChartSelected.lineChartOptions =  _dataChartSelected.lineChartOptions;
          break;

        case 'pata3':
          this.titlePataSelected = 'Pata 3';
          _dataChartSelected = this.setChart(this.angulo31,this.angulo32,this.hora,'Hora','Grados','Motor 1','Motor 2','#0C00FF','#FF0909')
          this.dataChartSelected.dataChartOptions =  _dataChartSelected.dataChartOptions;
          this.dataChartSelected.lineChartOptions =  _dataChartSelected.lineChartOptions;
          break;

        case 'pata4':
          this.titlePataSelected = 'Pata 4';
          _dataChartSelected = this.setChart(this.angulo41,this.angulo42,this.hora,'Hora','Grados','Motor 1','Motor 2','#0C00FF','#FF0909')
          this.dataChartSelected.dataChartOptions =  _dataChartSelected.dataChartOptions;
          this.dataChartSelected.lineChartOptions =  _dataChartSelected.lineChartOptions;
          break;
      }

      },
      error: err => {

      }
    })
  }

  loadData(){
    this.spinner.show();

    let obs: Observable<any>[] = [];
    obs.push(this.modosService.GetModoActual());
    obs.push(this.modosService.GetModos());
    obs.push(this.puntosService.GetPuntosById(1));

    forkJoin(obs).subscribe({
      next: response => {
        this.modoIdAnterior = response[0].id;
        this.secionIdActiva = response[0].seccionId;
        if(response[0] == null){
          this.isChecked = false
        }
        else{
          this.isChecked = true
        }

        this.PuntosDefinidos = response[1].filter((elemento) => elemento.seccionId === 1 || elemento.seccionId === 2);
        
        this.MarchasDefinidas = response[1].filter((elemento) => elemento.seccionId === 4);

        this.puntosHome = response[2][0];

        // this.patasForm.patchValue({
        //   P1X: this.puntosHome.p1X -3,
        //   P1Y: this.puntosHome.p1Y,
        //   P2X: this.puntosHome.p2X +3,
        //   P2Y: this.puntosHome.p2Y-1,
        //   P3X: this.puntosHome.p3X -3,
        //   P3Y: this.puntosHome.p3Y -1,
        //   P4X: this.puntosHome.p4X,
        //   P4Y: this.puntosHome.p4Y
        // });

        // this.patasForm.patchValue({
        //   P1X: this.puntosHome.p1X ,
        //   P1Y: this.puntosHome.p1Y,
        //   P2X: this.puntosHome.p2X,
        //   P2Y: this.puntosHome.p2Y,
        //   P3X: this.puntosHome.p3X,
        //   P3Y: this.puntosHome.p3Y,
        //   P4X: this.puntosHome.p4X,
        //   P4Y: this.puntosHome.p4Y
        // });
        


        switch (this.secionIdActiva) {
          case 1:
            this.operationMode = 'Puntos'
            break;
          case 2:
            this.operationMode = 'Puntos'
            break;
          case 3:
            this.operationMode = 'Manual'
            break;
          case 4:
            this.operationMode = 'Definidas'
            break;
        }

        // this.toastr.success(this.isChecked == true ? "Robot encendido con éxtio" : "Robot apagado con éxito");
        this.spinner.hide();
      },
      error: err => {
        this.spinner.hide();
        console.log(err);
        this.toastr.error(err);
      }
    });

  }

  onToggle() {
    this.spinner.show();
    let modo: ModosModel = {
      id:1,
      activo: this.isChecked
    }

    let obs: Observable<any>[] = [];
    obs.push(this.modosService.ActualizarModo(modo));

    forkJoin(obs).subscribe({
      next: response => {
        this.toastr.success(this.isChecked == true ? "Robot encendido con éxito" : "Robot apagado con éxito");
        this.loadData();
        this.spinner.hide();
      },
      error: err => {
        console.log(err);
        this.toastr.error(err);
        this.spinner.hide();
      }
    });
  }

  changeModoOperacion(modo: string){
    this.operationMode = modo;
  }

  updatePunto(select: any){
    this.spinner.show();
    let modo: ModosModel = {
      id:select.id,
      activo: !select.activo
    }

    let obs: Observable<any>[] = [];
    obs.push(this.modosService.ActualizarModo(modo));

    forkJoin(obs).subscribe({
      next: response => {
        this.loadData();
        this.toastr.success(this.isChecked == true ? "Modo de operación activado con éxito" : "Robot apagado con éxito");
        this.spinner.hide();
      },
      error: err => {
        console.log(err);
        this.toastr.error(err);
        this.spinner.hide();
      }
    });
  }

  sendData(){
    this.spinner.show();


    // let puntosPata: PuntosModel ={
    //   id: 10,
    //   p1X: this.patasForm.get('P1X').value == this.puntosHomeAjuste[0] ? this.puntosHome.p1X : this.patasForm.get('P1X').value +3,
    //   p1Y: this.patasForm.get('P1Y').value == this.puntosHomeAjuste[1] ? this.puntosHome.p1Y : this.patasForm.get('P1Y').value,
    //   p2X: this.patasForm.get('P2X').value == this.puntosHomeAjuste[0] ? this.puntosHome.p2X : this.patasForm.get('P2X').value-3,
    //   p2Y: this.patasForm.get('P2Y').value == this.puntosHomeAjuste[1] ? this.puntosHome.p2Y : this.patasForm.get('P2Y').value+1,
    //   p3X: this.patasForm.get('P3X').value == this.puntosHomeAjuste[0] ? this.puntosHome.p3X : this.patasForm.get('P3X').value+3,
    //   p3Y: this.patasForm.get('P3Y').value == this.puntosHomeAjuste[1] ? this.puntosHome.p3Y : this.patasForm.get('P3Y').value+1,
    //   p4X: this.patasForm.get('P4X').value == this.puntosHomeAjuste[0] ? this.puntosHome.p4X : this.patasForm.get('P4X').value,
    //   p4Y: this.patasForm.get('P4Y').value == this.puntosHomeAjuste[1] ? this.puntosHome.p4Y : this.patasForm.get('P4Y').value
    // }

    let puntosPata: PuntosModel ={
      id: 10,
      p1X: this.patasForm.get('P1X').value == null ? this.puntosHome.p1X : this.patasForm.get('P1X').value,
      p1Y: this.patasForm.get('P1Y').value == null ? this.puntosHome.p1Y : this.patasForm.get('P1Y').value,
      p2X: this.patasForm.get('P2X').value == null ? this.puntosHome.p2X : this.patasForm.get('P2X').value,
      p2Y: this.patasForm.get('P2Y').value == null ? this.puntosHome.p2Y : this.patasForm.get('P2Y').value,
      p3X: this.patasForm.get('P3X').value == null ? this.puntosHome.p3X : this.patasForm.get('P3X').value,
      p3Y: this.patasForm.get('P3Y').value == null ? this.puntosHome.p3Y : this.patasForm.get('P3Y').value,
      p4X: this.patasForm.get('P4X').value == null ? this.puntosHome.p4X : this.patasForm.get('P4X').value,
      p4Y: this.patasForm.get('P4Y').value == null ? this.puntosHome.p4Y : this.patasForm.get('P4Y').value
    }

    console.log("PUNTOS ENVIADOS: ",puntosPata)


    let obs: Observable<any>[] = [];
    obs.push(this.puntosService.ActualizarPunto(puntosPata));

    forkJoin(obs).subscribe({
      next: response => {
        this.loadData();

        this.toastr.success("Se han enviado correctamente los puntos en el modo manual.");
        this.spinner.hide();
      },
      error: err => {
        console.log(err);
        this.toastr.error(err);
        this.spinner.hide();
      }
    });
  }

  setChart(_data_y: number[], _data_y2: number[], _data_x: string[], _axisX: string, _axisY: string, _label: string,_label2:string, _color: string, _color2: string): ChartDataCustom{
    

    const chartData: ChartDataCustom = {};

    chartData.dataChartOptions = {
      datasets: 
      [ 
        {data: _data_y,label:_label,type:'line',borderColor:_color,backgroundColor:_color}, 
        {data: _data_y2,label:_label2,type:'line',borderColor:_color2,backgroundColor:_color2},
      ],
      labels: _data_x

    }

    chartData.lineChartOptions = {xAxisTitle: _axisX,yAxisTitle: _axisY,layoutPosition: 'bottom'};

    return chartData;
  }

  changeChart(pataSelected:string){
    this.pataSelected = pataSelected;
  }

}
