export const createPolylineStyle = (segment) => {
    let color = setColor(segment);
    let purpleColor = 'rgba(128, 0, 128, 0.8)';
    color = segment.average_grade > 0 ? purpleColor : color;
    return new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: color,
            width: 3,
        }),
    });
};

export const createPolyline = (segment, latlngs) =>
    new ol.Feature({
        geometry: new ol.geom.LineString(latlngs),
        ...segment,
    });

const setColor = (segment) => {
    if (segment.difficulty === 'green') {
        return 'rgba(70, 180, 20, 1)';
    } else if (segment.difficulty === 'blue') {
        return 'rgba(20, 140, 240, 1)';
    } else if (segment.difficulty === 'red') {
        return 'rgba(220, 19, 19, 1)';
    } else if (segment.difficulty === 'black') {
        return 'rgba(0, 0, 0, 1)';
    } else {
        return 'rgba(220, 19, 19, 1)'; // default to red
    }
};
