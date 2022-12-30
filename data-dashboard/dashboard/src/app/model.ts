export interface TemperatureRawDataPoint {
  _id: string;
  metadata: {
    sensor_area: string;
  }
  temperature: number;
  timestamp: string;
}

export interface TemperatureDataPoint {
  id: string;
  metadata: {
    sensor_area: string;
  }
  temperature: number;
  timestamp: Date;
}
