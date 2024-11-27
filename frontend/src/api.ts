import { TrailArea } from './types/TrailArea';
import { Segment } from './types/Segment';

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

export const fetchAreaSegments = async (location: string): Promise<Segment[]> => {
    try {
        const response = await fetch(`/api/segments/${location}`);
        if (!response.ok) {
            throw new Error(
                `Error fetching ${location} area segments: ${response.statusText}`
            );
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
        throw error;
    }
}