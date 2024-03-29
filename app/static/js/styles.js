export const createPolylineStyle = (segment) => {
    let redColor = 'rgba(255, 0, 0, 0.8)';
    let purpleColor = 'rgba(128, 0, 128, 0.8)';
    let color = segment.average_grade > 0 ? purpleColor : redColor;
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
