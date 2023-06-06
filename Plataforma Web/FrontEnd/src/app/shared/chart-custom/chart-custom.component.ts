import { Component, Input, OnChanges, OnInit } from '@angular/core';
import { ChartConfiguration, ChartData, ChartType } from 'chart.js';
import { ChartDataCustom } from 'src/app/models/ChartDataCustom';
import { SetChartOptionsService } from 'src/app/services/set-chart-options.service';

@Component({
  selector: 'app-chart-custom',
  templateUrl: './chart-custom.component.html'
})
export class ChartCustomComponent implements  OnChanges{

  lineChartOptions: ChartConfiguration['options'];
  consumoActualChart: ChartType = 'line';

  consumoActualData: ChartData;

  @Input() setChartOptions: ChartDataCustom;

  constructor(private setChartsOptionsService: SetChartOptionsService){

    this.consumoActualData  = {
      datasets: [
        {
          data: null,
          fill: false,
          borderColor: '#FF0909',
          label: '',
          pointStyle: false,
          backgroundColor: '#FF0909',

        }, {
          data: null,
          fill: false,
          borderColor: '#0C00FF',
          label: '',
          pointStyle: false,
          backgroundColor: '#0C00FF',
        }, {
          data: null,
          fill: false,
          borderColor: '#F48023',
          label: '',
          pointStyle: false,
          backgroundColor: '#F48023',
        }
      ],
      labels: []
    }

    this.lineChartOptions= {maintainAspectRatio: false}
    
  }

  ngOnChanges(){


    try {
      if(this.setChartOptions.lineChartOptions !== undefined){
        this.lineChartOptions = this.setChartsOptionsService.setLineChartOption({
          xAxisTitle: this.setChartOptions.lineChartOptions.xAxisTitle,
          yAxisTitle: this.setChartOptions.lineChartOptions.yAxisTitle,
          layoutPosition: this.setChartOptions.lineChartOptions.layoutPosition,
          
          suggestedMin: this.setChartOptions.lineChartOptions.suggestedMin != undefined ? this.setChartOptions.lineChartOptions.suggestedMin : null,
          suggestedMax: this.setChartOptions.lineChartOptions.suggestedMax != undefined ? this.setChartOptions.lineChartOptions.suggestedMax : null
        });
    
        if(this.setChartOptions.dataChartOptions.datasets.length < this.consumoActualData.datasets.length){
          this.consumoActualData.datasets.splice(this.setChartOptions.dataChartOptions.datasets.length, this.consumoActualData.datasets.length - this.setChartOptions.dataChartOptions.datasets.length)
        }
    
        for (let i = 0; i < (this.setChartOptions.dataChartOptions.datasets.length > 3 ? 3 : this.setChartOptions.dataChartOptions.datasets.length); i++) {

          this.consumoActualData.datasets[i].data = this.setChartOptions.dataChartOptions.datasets[i].data
          this.consumoActualData.datasets[i].label = this.setChartOptions.dataChartOptions.datasets[i].label;
          this.consumoActualData.datasets[i].type = this.setChartOptions.dataChartOptions.datasets[i].type;
          this.consumoActualData.datasets[i].hidden = this.setChartOptions.dataChartOptions.datasets[i].hidden != undefined ? this.setChartOptions.dataChartOptions.datasets[i].hidden : false;


          if(this.setChartOptions.dataChartOptions.datasets[i].backgroundColor !== undefined){
            this.consumoActualData.datasets[i].backgroundColor = this.setChartOptions.dataChartOptions.datasets[i].backgroundColor;
          }

          if(this.setChartOptions.dataChartOptions.datasets[i].borderColor !== undefined){
            this.consumoActualData.datasets[i].borderColor = this.setChartOptions.dataChartOptions.datasets[i].borderColor;
          }
        }
    
        this.consumoActualData.labels = this.setChartOptions.dataChartOptions.labels
      }
    } catch (error) {
      console.log(error)
    }


  }


}

