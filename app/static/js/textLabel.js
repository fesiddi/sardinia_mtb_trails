export function createTextStyle(segmentName) {
    return new ol.style.Style({
        text: new ol.style.Text({
            text: segmentName,
            font: '11px sans-serif',
            placement: 'line',
            rotateWithView: false,
            overflow: true,
            fill: new ol.style.Fill({ color: 'lightgreen' }),
            stroke: new ol.style.Stroke({ color: 'black', width: 4 }),
        }),
    });
}

export function createTextLabelLayer(coordinates, segment) {
    const geometry = new ol.geom.LineString(coordinates);
    const feature = new ol.Feature({ geometry, ...segment });
    feature.setStyle(createTextStyle(segment.name));

    const source = new ol.source.Vector({
        features: [feature],
    });

    const layer = new ol.layer.Vector({
        source: source,
        visible: true,
        zIndex: 1000,
        declutter: true,
    });

    return layer;
}
