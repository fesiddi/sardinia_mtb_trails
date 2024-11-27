import { Map, Overlay } from 'ol';
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
    content.className = styles.olPopupContent;
    return content;
}

function handleMapClick(
    evt: any,
    mapInstance: Map,
    popup: Overlay,
    content: HTMLElement
) {
    console.log('Map clicked at', evt.pixel);
    const feature = mapInstance.forEachFeatureAtPixel(evt.pixel,(feature) => feature);

    if (feature) {
        console.log('Feature clicked!');
        showPopup(popup, evt.coordinate, feature, content);
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
        if (feature.get('type') === 'trailBase') {
            content.innerHTML = generateTrailBaseContent(feature);
            popup.setPosition(coordinates);
        } else if (feature.get('type') === 'segment') {
            content.innerHTML = generateSegmentContent(feature);
            popup.setPosition(coordinates);
        }
    } else {
        console.error('Popup content element not found');
        throw new Error('Popup content element not found');
    }
}

function generateTrailBaseContent(feature: any) {
    const trailBase = feature.get('trailBaseProps');
    console.log('Trail Base properties: ', trailBase);
    const [longitude, latitude] = trailBase.coordinates;
    const googleMapsLink = `https://www.google.com/maps?q=${latitude},${longitude}`;
    return `
        <h4><strong>${
            trailBase.name || 'Trail Base'
        }</strong></h4>
        <a href="${googleMapsLink}" target="_blank">View in Maps</a>
    `;
}

function generateSegmentContent(feature: any) {
    const segment = feature.get('segmentProps');
    console.log('Segment properties: ', segment);
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
