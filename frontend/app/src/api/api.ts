
import apiClient from "@/utils/axios";
import { Breach } from "@/models/Breach";
import { AxiosInstance } from "axios";

export enum QueryType {
    Email,
    Rut,
    Phone
}

export async function getBreachesByQueryType(query: string, type: QueryType): Promise<Breach[]> {
    let response;
    const data = {"value": query};
    try {
        switch (type) {
            case QueryType.Email:
                response = await apiClient.post<Breach[]>("/breach/email/", data);
                return response.data;
            case QueryType.Rut:
                // response = await apiClient.get<Breach[]>(`/breach/rut/${query}`);
                response = await apiClient.post<Breach[]>("/breach/rut/", data);
                return response.data;
            case QueryType.Phone:
                response = await apiClient.post<Breach[]>("/breach/phone/", data);
                return response.data;
            default:
                return [];
        }
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

// export async function getBreachesByEmail(email: string, queryType: QueryType): Promise<Breach[]> {
//     try {
//         switch (queryType) {
//             case QueryType.Email:
                
//                 break;
//             case QueryType.Rut:
                
//                 break;
//             case QueryType.Phone:
                
//                 break;
        
//             default:
//                 break;
//         }
//         const response = await apiClient.get<Breach[]>(`/breach/email/${email}`);
//         return response.data;
//     } catch (error: any) {
//         if (error.response && error.response.status === 404) {
//             return [];
//         } else {
//             // TODO: Informar que ha ocurrido un error
//             return [];
//             // throw error;
//         }
//     }
// }