export const createMarkerStyle = () =>
    new ol.style.Style({
        image: new ol.style.Circle({
            radius: 4,
            fill: new ol.style.Fill({ color: 'yellow' }),
            stroke: new ol.style.Stroke({
                color: 'black',
                width: 1,
            }),
        }),
    });

export const createMarker = (start_latlng) =>
    new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat(start_latlng)),
    });

export const createLayer = (features) =>
    new ol.layer.Vector({
        source: new ol.source.Vector({ features }),
    });
