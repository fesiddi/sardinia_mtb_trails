import { Map, Overlay } from 'ol';
import Point from 'ol/geom/Point';
import { fromLonLat, toLonLat } from 'ol/proj';
import 'ol/ol.css';
import styles from '../components/TrailAreaMap.module.css';

export const initializePopup = (mapInstance: Map) => {
    console.log('Initializing popup');

    const popupElement = createPopupElement();
    document.body.appendChild(popupElement);

    const popup = new Overlay({
        element: popupElement,
        positioning: 'bottom-center',
        stopEvent: false,
        offset: [0, -10],
    });

    mapInstance.addOverlay(popup);
    console.log('Popup overlay added to map');

    const closer = createCloserElement(popup);
    popupElement.appendChild(closer);

    const content = createContentElement();
    popupElement.appendChild(content);

    mapInstance.on('click', (evt) =>
        handleMapClick(evt, mapInstance, popup, content)
    );
};


function createPopupElement() {
    const popupElement = document.createElement('div');
    popupElement.className = styles.olPopup;
    return popupElement;
}

function createCloserElement(popup: Overlay) {
    const closer = document.createElement('a');
    closer.href = '#';
    closer.className = styles.olPopupCloser;
    closer.innerHTML = '✖';
    closer.onclick = () => {
        console.log('Popup closer clicked');
        popup.setPosition(undefined);
        closer.blur();
        return false;
    };
    return closer;
}

function createContentElement() {
    const content = document.createElement('div');
    return content;
}

function handleMapClick(
    evt: any,
    mapInstance: Map,
    popup: Overlay,
    content: HTMLElement
) {
    console.log('Map clicked at', evt.pixel);
    const feature = mapInstance.forEachFeatureAtPixel(
        evt.pixel,
        (feature) => feature
    );

    if (feature) {
        console.log('Feature clicked:', feature);
        const featureProperties = feature.getProperties();
        console.log('Feature properties: ', featureProperties);
        const geometry = feature.getGeometry() as Point;
        const coordinates = geometry.getCoordinates();
        showPopup(popup, coordinates, feature, content);
    } else {
        console.log('No feature clicked');
    }
}

function showPopup(
    popup: Overlay,
    coordinates: number[],
    feature: any,
    content: HTMLElement
) {
    if (content) {
        if (feature.get('type') === 'trailBaseMarker') {
            content.innerHTML = generateTrailBaseContent(
                feature,
                coordinates
            );
            popup.setPosition(coordinates);
            console.log('Popup position set to:', coordinates);
        } else if (feature.get('type') === 'segment') {
            console.log('content is a segment');
            content.innerHTML = generateSegmentContent(feature);
            const segment = feature.get('segment');
            const startLat = segment.start_lat;
            const startLon = segment.start_lng;
            popup.setPosition(fromLonLat([startLon, startLat]));
            console.log('Popup position set to:', startLat, startLon);
        }
    } else {
        console.error('Popup content element not found');
        throw new Error('Popup content element not found');
    }
}

function generateTrailBaseContent(feature: any, coordinates: number[]) {
    const properties = feature.getProperties();
    console.log('Trail Base properties: ', properties);
    const [longitude, latitude] = toLonLat(coordinates);
    const googleMapsLink = `https://www.google.com/maps?q=${latitude},${longitude}`;
    return `
        <h4><strong>${properties.name || 'Trail Base Marker'}</strong></h4>
        <a href="${googleMapsLink}" target="_blank">View in Maps</a>
    `;
}

function generateSegmentContent(feature: any) {
    const segment = feature.get('segment');
    console.log('Segment content: ', segment);
    return `
    <h4><strong>${segment.alt_name}</strong></h4>
    <p><strong>KOM: </strong>${segment.kom}</p>
    <p><strong>Athletes Count: </strong>${segment.athlete_count}</p>
    ${
        segment.local_legend &&
        segment.local_legend.title &&
        segment.local_legend.athlete_id
            ? `<p><strong>Local Legend: </strong><a href="https://www.strava.com/athletes/${segment.local_legend.athlete_id}">${segment.local_legend.title}</a></p>`
            : ''
    }
    <p>${
        segment.local_legend ? segment.local_legend.effort_description : ''
    }</p>
    <p><a href="https://www.strava.com/segments/${
        segment.id
    }">View Segment on Strava</a></p>
`;
}
