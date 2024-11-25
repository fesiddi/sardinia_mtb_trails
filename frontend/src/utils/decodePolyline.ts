import { fromLonLat } from 'ol/proj';

/**
 * Decodes a polyline encoded string into an array of coordinates.
 * The encoded string is typically used to represent a series of latitude and longitude points.
 * This function converts the encoded string into an array of [longitude, latitude] tuples.
 *
 * @param encoded - The encoded polyline string.
 * @returns An array of [longitude, latitude] tuples representing the decoded polyline.
 */
export function decodePolyline(encoded: string): Array<[number, number]> {
    const points: Array<[number, number]> = [];
    let index = 0,
        len = encoded.length;
    let lat = 0,
        lng = 0;

    while (index < len) {
        let b,
            shift = 0,
            result = 0;
        do {
            b = encoded.charAt(index++).charCodeAt(0) - 63;
            result |= (b & 0x1f) << shift;
            shift += 5;
        } while (b >= 0x20);
        const dlat = (result & 1) !== 0 ? ~(result >> 1) : result >> 1;
        lat += dlat;

        shift = 0;
        result = 0;
        do {
            b = encoded.charAt(index++).charCodeAt(0) - 63;
            result |= (b & 0x1f) << shift;
            shift += 5;
        } while (b >= 0x20);
        const dlng = (result & 1) !== 0 ? ~(result >> 1) : result >> 1;
        lng += dlng;

        points.push(fromLonLat([lng / 1e5, lat / 1e5]) as [number, number]);
    }
    return points;
}
