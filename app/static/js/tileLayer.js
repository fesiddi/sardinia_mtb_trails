export const createTileLayer = () =>
    new ol.layer.Tile({
        source: new ol.source.OSM(),
    });
