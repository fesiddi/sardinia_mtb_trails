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

    popoverElement.style.position = 'absolute';
    popoverElement.style.left = `${left}px`;
    popoverElement.style.top = `${top}px`;

    popoverInstance.show();
}

function disposePopover() {
    if (popoverInstance) {
        popoverInstance.dispose();
        popoverElement.remove();
        popoverInstance = null;
        popoverElement = null;
    }
}

function calculatePopoverPosition(map, coordinates) {
    const pixel = map.getPixelFromCoordinate(coordinates);
    const rect = map.getTargetElement().getBoundingClientRect();
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
    const { name, id, kom, athlete_count, local_legend } =
        feature.getProperties();

    return `
    <h4><strong>${name}</strong></h4>
    <p><strong>KOM: </strong>${kom}</p>
    <p><strong>Athletes Count: </strong>${athlete_count}</p>
    ${
        local_legend && local_legend.title && local_legend.athlete_id
            ? `<p><strong>Local Legend: </strong><a href="https://www.strava.com/athletes/${local_legend.athlete_id}">${local_legend.title}</a></p>`
            : ''
    }
    <p>${local_legend ? local_legend.effort_description : ''}</p>
    <p><a href="https://www.strava.com/segments/${id}">View Segment on Strava</a></p>
  `;
}
