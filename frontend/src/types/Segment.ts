export interface EffortCounts {
    overall: string;
    female: string | null;
}

export interface LocalLegend {
    athlete_id: number;
    title: string;
    profile: string;
    effort_description: string;
    effort_count: string;
    effort_counts: EffortCounts;
    destination: string;
}

export interface Map {
    id: string;
    polyline: string;
    resource_state: number;
}

export interface Segment {
    id: number;
    name: string;
    alt_name: string;
    trail_area: string;
    average_grade: number;
    distance: number;
    difficulty: string;
    popularity: number;
    start_lat: number;
    start_lng: number;
    end_lat: number;
    end_lng: number;
    local_legend: LocalLegend | null;
    star_count: number;
    effort_count: number;
    athlete_count: number;
    kom: string;
    map: Map;
    polyline: string;
    timestamp: number;
}
