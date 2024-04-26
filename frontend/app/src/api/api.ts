import { Breach } from "@/models/Breach";
import apiClient from "@/utils/axios";

export enum QueryType {
  Email,
  Rut,
  Phone,
}

// TODO: Change Promise for DataLeak Interface
export async function getBreachesByQueryType(
  query: string,
  type: QueryType
): Promise<Breach[]> {
  let response;
  const data = { hash_value: query };
  try {
    response = await apiClient.post<Breach[]>("/breach/data/", data);
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
