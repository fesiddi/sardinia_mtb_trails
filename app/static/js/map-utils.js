const TILE_SERVER_URL =
    'https://tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=52c2b5d8de3e4f1ab03dc1e108cd1a3d';

export const initMap = (firstSegmentLng, firstSegmentLat, target, segments) => {
    const map = new ol.Map({
        target: target,
        layers: [createTileLayer()],
        view: new ol.View({
            center: ol.proj.fromLonLat([firstSegmentLng, firstSegmentLat]),
            zoom: 13,
        }),
    });

    map.once('postrender', () => addPolylineLayers(map, segments));
    fitMapToSegments(map, segments);

    return map;
};

const calculateBounds = (segments) =>
    segments.reduce(
        (bounds, { start_lng, start_lat, end_lng, end_lat }) => [
            Math.min(bounds[0], start_lng, end_lng),
            Math.min(bounds[1], start_lat, end_lat),
            Math.max(bounds[2], start_lng, end_lng),
            Math.max(bounds[3], start_lat, end_lat),
        ],
        [
            segments[0].start_lng,
            segments[0].start_lat,
            segments[0].end_lng,
            segments[0].end_lat,
        ]
    );

const fitMapToSegments = (map, segments) => {
    let bounds = calculateBounds(segments);
    bounds = ol.proj.transformExtent(
        bounds,
        'EPSG:4326',
        map.getView().getProjection()
    );
    map.getView().fit(bounds, { padding: [50, 50, 50, 50] });
};

const createTileLayer = () =>
    new ol.layer.Tile({
        source: new ol.source.XYZ({ url: TILE_SERVER_URL }),
    });

export const addPolylineLayers = (map, segments) => {
    segments.forEach((segment) => {
        const { start_lat, start_lng, polyline } = segment;
        const start_latlng = [start_lng, start_lat];
        const marker = createMarker(start_latlng);
        const markerLayer = createLayer([marker]);

        marker.setStyle(createMarkerStyle());
        map.addLayer(markerLayer);

        const latlngs = decode(polyline);
        const decodedPolyline = createPolyline(segment, latlngs);

        decodedPolyline.setStyle(createPolylineStyle(segment));

        const polylineLayer = createLayer([decodedPolyline]);

        map.addLayer(polylineLayer);

        const textLayer = createTextLabelLayer(latlngs, segment);
        map.addLayer(textLayer);
        map.renderSync();
    });
};

const createMarkerStyle = () =>
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

const createPolylineStyle = (segment) => {
    let redColor = 'rgba(255, 0, 0, 0.8)';
    let purpleColor = 'rgba(128, 0, 128, 0.8)';
    let color = segment.average_grade > 0 ? purpleColor : redColor; // change color based on average_grade
    return new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: color,
            width: 3,
        }),
    });
};

const createPolyline = (segment, latlngs) =>
    new ol.Feature({
        geometry: new ol.geom.LineString(latlngs),
        ...segment,
    });

const createMarker = (start_latlng) =>
    new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat(start_latlng)),
    });

const createLayer = (features) =>
    new ol.layer.Vector({
        source: new ol.source.Vector({ features }),
    });

export function decode(encoded) {
    var points = [];
    var index = 0,
        len = encoded.length;
    var lat = 0,
        lng = 0;

    while (index < len) {
        var b,
            shift = 0,
            result = 0;
        do {
            b = encoded.charAt(index++).charCodeAt(0) - 63;
            result |= (b & 0x1f) << shift;
            shift += 5;
        } while (b >= 0x20);
        var dlat = (result & 1) != 0 ? ~(result >> 1) : result >> 1;
        lat += dlat;

        shift = 0;
        result = 0;
        do {
            b = encoded.charAt(index++).charCodeAt(0) - 63;
            result |= (b & 0x1f) << shift;
            shift += 5;
        } while (b >= 0x20);
        var dlng = (result & 1) != 0 ? ~(result >> 1) : result >> 1;
        lng += dlng;

        points.push(ol.proj.fromLonLat([lng / 1e5, lat / 1e5]));
    }
    return points;
}

export const setupPopup = (map, mapId) => {
    const popup = createPopup(mapId);
    map.addOverlay(popup);

    map.on('click', (evt) => handleMapClick(evt, map, popup));
};

const createPopup = (mapId) => {
    const popupElement = document.createElement('div');
    popupElement.id = `popup-${mapId}`;
    popupElement.className = 'popup';
    document.body.appendChild(popupElement);

    return new ol.Overlay({
        element: popupElement,
        positioning: 'bottom-center',
        stopEvent: false,
        offset: [0, -10],
    });
};

let popoverInstance = null;
let popoverElement = null;

function createPopover(feature, map, coordinates) {
    // Create a new element for the popover
    popoverElement = document.createElement('div');
    popoverElement.id = 'popover';
    map.getTargetElement().appendChild(popoverElement);

    const content = generatePopupContent(feature);
    popoverInstance = new bootstrap.Popover(popoverElement, {
        placement: 'top',
        html: true,
        content: content,
        customClass: 'popover',
    });

    const [left, top] = calculatePopoverPosition(map, coordinates);

    // Set the position of the popover element
    popoverElement.style.position = 'absolute';
    popoverElement.style.left = `${left}px`;
    popoverElement.style.top = `${top}px`;

    popoverInstance.show();
}
// Create a style function that returns a style with a text label
function createTextStyle(segmentName) {
    return new ol.style.Style({
        text: new ol.style.Text({
            text: segmentName,
            font: '11px sans-serif',
            placement: 'line', // Make the text follow the line
            rotateWithView: false,
            overflow: true,
            fill: new ol.style.Fill({ color: 'lightgreen' }),
            stroke: new ol.style.Stroke({ color: 'black', width: 4 }),
        }),
    });
}

function createTextLabelLayer(coordinates, segment) {
    // Create a line geometry with the given coordinates
    const geometry = new ol.geom.LineString(coordinates);

    // Create a feature with the line geometry
    const feature = new ol.Feature({ geometry, ...segment });

    // Set the style of the feature to the text style
    feature.setStyle(createTextStyle(segment.name));

    // Create a source and add the feature to it
    const source = new ol.source.Vector({
        features: [feature],
    });

    // Create a layer and add the source to it
    const layer = new ol.layer.Vector({
        source: source,
        visible: true,
        zIndex: 1000,
        declutter: true,
    });

    return layer;
}

function disposePopover() {
    // Dispose of the existing popover instance and remove the element
    if (popoverInstance) {
        popoverInstance.dispose();
        popoverElement.remove();
        popoverInstance = null;
        popoverElement = null;
    }
}

function calculatePopoverPosition(map, coordinates) {
    // Convert map coordinates to pixel coordinates
    const pixel = map.getPixelFromCoordinate(coordinates);

    // Get the position of the map within the viewport
    const rect = map.getTargetElement().getBoundingClientRect();

    // Adjust the pixel coordinates based on the position of the map
    const left = rect.left + pixel[0] + window.scrollX;
    const top = rect.top + pixel[1] + window.scrollY;

    return [left, top];
}

function handleMapClick(evt, map, popup) {
    const feature = map.forEachFeatureAtPixel(evt.pixel, (feature) => feature);

    disposePopover();
    if (feature && feature.getGeometry().getType() === 'LineString') {
        const coordinates = evt.coordinate;
        popup.setPosition(coordinates);
        createPopover(feature, map, coordinates);
    } else {
        popup.setPosition(undefined);
    }
}

function generatePopupContent(feature) {
    const { name, star_count, kom, athlete_count, local_legend, segmentId } =
        feature.getProperties();

    return `
        <h5><strong>${name}</strong></h5>
        <p><strong>KOM: </strong>${kom}</p>
        <p><strong>Stars Count: </strong>${star_count}</p>
        <p><strong>Athletes Count: </strong>${athlete_count}</p>
        ${
            local_legend && local_legend.title && local_legend.athlete_id
                ? `<p><strong>Local Legend: </strong><a href="https://www.strava.com/athletes/${local_legend.athlete_id}">${local_legend.title}</a></p>`
                : ''
        }
        <p>${local_legend ? local_legend.effort_description : ''}</p>
        <p><a href="https://www.strava.com/segments/${segmentId}">View Segment on Strava</a></p>
    `;
}
