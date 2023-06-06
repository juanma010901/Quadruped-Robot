import { Injectable } from '@angular/core';
import { ChartConfiguration } from 'chart.js';
import { ChartOptionsParamaters } from '../models/ChartOptionsParameters';

@Injectable({
  providedIn: 'root'
})
export class SetChartOptionsService {

  private lineChartOptions: ChartConfiguration['options']
  constructor() { }

  public setLineChartOption(optionsParamaters: ChartOptionsParamaters): ChartConfiguration['options'] {
    this.lineChartOptions = {
      responsive: optionsParamaters.responsive ? optionsParamaters.responsive : true,
      maintainAspectRatio: optionsParamaters.maintainAspectRatio ? optionsParamaters.maintainAspectRatio : false,
      elements: {
        line: {
          tension: optionsParamaters.lineTension
        }
      },
      scales: {
        x: {
          title: {
            display: optionsParamaters.xAxisDisplay ? optionsParamaters.xAxisDisplay : true,
            text: optionsParamaters.xAxisTitle
          },
          ticks: {
            autoSkip: true,
            align: 'start',
            autoSkipPadding: 15
          }
        },
        y: {
          beginAtZero: false,
          position: 'left',
          title: {
            display: optionsParamaters.yAxisDisplay ? optionsParamaters.yAxisDisplay : true,
            text: optionsParamaters.yAxisTitle
          },
          suggestedMin: optionsParamaters.suggestedMin != null ? optionsParamaters.suggestedMin : null,
          suggestedMax: optionsParamaters.suggestedMax != null ? optionsParamaters.suggestedMax : null
        }
      },
      plugins: {
        legend: {
          display: optionsParamaters.displayLegend,
          position: optionsParamaters.layoutPosition,
          labels: {
            font: {
              size: optionsParamaters.layoutFontSize ? optionsParamaters.layoutFontSize : 16,
              family: optionsParamaters.layoutFamily ? optionsParamaters.layoutFamily : 'Poppins'
            }
          }
        }
      }
    }

    return this.lineChartOptions;
  }
}
