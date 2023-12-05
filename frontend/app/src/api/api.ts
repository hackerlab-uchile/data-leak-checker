
import apiClient from "@/utils/axios";
import { Breach } from "@/models/Breach";

export async function getBreachesByEmail(email: string): Promise<Breach[]> {
    try {
        const response = await apiClient.get<Breach[]>(`/breach/email/${email}`);
        return response.data;
    } catch (error: any) {
        if (error.response && error.response.status === 404) {
            return [];
        } else {
            throw error;
        }
    }
}