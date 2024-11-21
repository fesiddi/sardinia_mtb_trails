export interface LocalRider {
    name: string;
    strava_id: string;
}

export interface TrailBase {
    name: string;
    coordinates: [number, number];
}

export interface TrailArea {
    name: string;
    s_name: string;
    description: string;
    local_riders: LocalRider[];
    instagram: string[];
    trail_bases?: TrailBase[] | null;
}
