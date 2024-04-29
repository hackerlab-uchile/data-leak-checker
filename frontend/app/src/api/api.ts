import { DataLeak } from "@/models/Breach";
import apiClient from "@/utils/axios";

export enum QueryType {
  Email = "email",
  Rut = "rut",
  Phone = "phone",
}

export async function getDataLeaksByValueAndType(
  query: string,
  type: QueryType
): Promise<DataLeak[]> {
  let response;
  const data = { value: query, dtype: type };
  try {
    response = await apiClient.post<DataLeak[]>("/breach/data/", data);
    return response.data;
  } catch (error: any) {
    if (error.response && error.response.status === 404) {
      return [];
    } else {
      // TODO: Informar que ha ocurrido un error
      return [];
      // throw error;
    }
  }
}
