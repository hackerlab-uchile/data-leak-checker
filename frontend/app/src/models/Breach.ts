export interface Breach {
  id: number;
  name: string;
  description: boolean;
  // breach_date: Date;
  breach_date: string;
  created_at: string;
  data_types: string[];
}

export interface DataLeak {
  breach: Breach;
  found_with: string[];
}
