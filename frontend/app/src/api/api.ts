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
): Promise<[DataLeak[], boolean]> {
  let response;
  const data = { value: query, dtype: type };
  let got_error: boolean = false;
  try {
    response = await apiClient.post<DataLeak[]>("/breach/data/demo/", data);
    return [response.data, got_error];
  } catch (error: any) {
    got_error = true;
    if (error.response && error.response.status === 404) {
      return [[], got_error];
    } else {
      // TODO: Informar que ha ocurrido un error
      return [[], got_error];
      // throw error;
    }
  }
}

export async function getDataLeaksByValueAndTypeReal(
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

export async function sendVerificationEmail(query: string): Promise<string> {
  let response;
  const data = { email: query };
  try {
    response = await apiClient.post(`/verify/send/email/`, data);
    return "";
  } catch (error: any) {
    if (error.response && error.response.status === 422) {
      return "El formato del correo ingresado no es válido. Por favor, inténtelo de nuevo";
    } else {
      return "Ha ocurrido un error. Por favor, inténtelo más tarde";
    }
  }
}

export async function sendVerificationSMS(query: string): Promise<string> {
  let response;
  const data = { phone: query };
  try {
    response = await apiClient.post(`/verify/send/sms/`, data);
    return "";
  } catch (error: any) {
    if (error.response && error.response.status === 422) {
      return "El formato del número móvil ingresado no es válido. Por favor, inténtelo de nuevo";
    } else {
      return "Ha ocurrido un error. Por favor, inténtelo más tarde";
    }
  }
}
