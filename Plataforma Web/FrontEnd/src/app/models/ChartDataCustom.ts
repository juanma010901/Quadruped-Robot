import { ChartConfiguration, ChartData } from "chart.js";

export interface ChartDataCustom{
    lineChartOptions?: any;
    dataChartOptions?: ChartData;
    dataOptionsPrueba?: ChartData<'line'>;
}