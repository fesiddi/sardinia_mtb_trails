export const calculateBounds = (segments) => {
    let minLng = segments[0].start_lng;
    let minLat = segments[0].start_lat;
    let maxLng = segments[0].end_lng;
    let maxLat = segments[0].end_lat;

    segments.forEach(({ start_lng, start_lat, end_lng, end_lat }) => {
        minLng = Math.min(minLng, start_lng, end_lng);
        minLat = Math.min(minLat, start_lat, end_lat);
        maxLng = Math.max(maxLng, start_lng, end_lng);
        maxLat = Math.max(maxLat, start_lat, end_lat);
    });

    return [minLng, minLat, maxLng, maxLat];
};

export const calculateExtent = (bounds, factor = 10, minSize = 1) => {
    const centerX = (bounds[0] + bounds[2]) / 2;
    const centerY = (bounds[1] + bounds[3]) / 2;

    let width = (bounds[2] - bounds[0]) * factor;
    let height = (bounds[3] - bounds[1]) * factor;

    // Ensure the width and height are at least minSize
    width = Math.max(width, minSize);
    height = Math.max(height, minSize);

    return [
        centerX - width / 2,
        centerY - height / 2,
        centerX + width / 2,
        centerY + height / 2,
    ];
};
