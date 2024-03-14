
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
    try {
        switch (type) {
            case QueryType.Email:
                response = await apiClient.get<Breach[]>(`/breach/email/${query}`);
                return response.data;
            case QueryType.Rut:
                response = await apiClient.get<Breach[]>(`/breach/rut/${query}`);
                return response.data;
            case QueryType.Phone:
                response = await apiClient.get<Breach[]>(`/breach/phone/${query}`);
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