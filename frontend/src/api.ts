import { TrailArea } from './types/TrailArea';

export const fetchTrailAreas = async (): Promise<TrailArea[]> => {
    try {
        const response = await fetch('/api/trail-areas');
        if (!response.ok) {
            throw new Error(
                `Error fetching trail areas: ${response.statusText}`
            );
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
        throw error;
    }
};
