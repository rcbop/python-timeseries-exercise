export interface RawTemperatureDataPoint {
  _id: string;
  value: number;
  timestamp: string;
  metadata: {
    area: string;
    type: string;
    uuid: string;
  }
}

export interface TemperatureDataPoint {
  id: string;
  value: number;
  timestamp: Date;
  sensor_uuid: string;
  area: string;
  type: string;
}
