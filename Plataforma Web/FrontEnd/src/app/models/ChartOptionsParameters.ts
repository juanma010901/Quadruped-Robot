import { PointStyle, LayoutPosition, PointOptions } from 'chart.js';
export interface ChartOptionsParamaters {
    responsive?: boolean;
    maintainAspectRatio?: boolean;
    lineTension?: 0 | 0.1 | 0.5;
    xAxisDisplay?: boolean;
    yAxisDisplay?: boolean;
    xAxisTitle: string;
    yAxisTitle: string;
    layoutPosition: LayoutPosition;
    displayLegend?: boolean;
    layoutFontSize?: number;
    layoutFamily?: string;
    suggestedMin?: number;
    suggestedMax?: number;
}