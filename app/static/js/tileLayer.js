const TILE_SERVER_URL =
    'https://tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=52c2b5d8de3e4f1ab03dc1e108cd1a3d';

export const createTileLayer = () =>
    new ol.layer.Tile({
        source: new ol.source.XYZ({ url: TILE_SERVER_URL }),
    });
