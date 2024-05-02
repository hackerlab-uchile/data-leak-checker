export interface Breach {
  id: number;
  name: string;
  description: boolean;
  // breach_date: Date;
  breach_date: string;
  created_at: string;
  breached_data: string[];
  security_tips: string[];
}

export interface DataLeak {
  data_type: string;
  breach: Breach;
  found_with: string[];
}
