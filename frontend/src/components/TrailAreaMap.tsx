import React, { useEffect, useRef, useState } from 'react';
import 'ol/ol.css';
import { Map as OLMap } from 'ol';
import styles from './TrailAreaMap.module.css';
import { initializeMap } from '../utils/mapInitialization'
import { drawSegments } from '../utils/mapUtils';
import { Segment } from '../types/Segment';
import { fetchAreaSegments } from '../api';
import { TrailBase } from '../types/TrailArea';
import { initializePopup } from '../utils/popupUtils';

interface TrailAreaMapProps {
    areaShortName: string;
    trailBases: TrailBase[] | null | undefined;
}

const TrailAreaMap: React.FC<TrailAreaMapProps> = ({ areaShortName, trailBases }) => {
    const mapRef = useRef<HTMLDivElement | null>(null);
    const mapInstanceRef = useRef<OLMap | null>(null);
    const [segments, setSegments] = useState<Segment[]>([]);
    const [error, setError] = useState<string | null>(null);
    const hasFetchedSegments = useRef<boolean>(false); // Ref to track if segments have been fetched

    useEffect(() => {
        const getSegments = async () => {
            try {
                const data = await fetchAreaSegments(areaShortName);
                setSegments(data);
                setError(null);
            } catch (error) {
                console.error('Failed to fetch segments: ', error);
                setError('Failed to fetch segments');
                setSegments([]);
            }
        };
        if (!hasFetchedSegments.current) {
            getSegments();
            hasFetchedSegments.current = true;
        }
    }, [areaShortName]);

    useEffect(() => {
        if (!mapRef.current || segments.length === 0) return;

        const firstSegment = segments[0];
        const { start_lat, start_lng } = firstSegment;

        console.log('Initializing map');
        const mapInstance = initializeMap(mapRef.current, start_lng, start_lat);
        mapInstanceRef.current = mapInstance;

        initializePopup(mapInstance);

        return () => {
            console.log('Cleaning up map');
            mapInstance.setTarget(undefined);
        };
    }, [segments]);


  useEffect(() => {
      if (mapInstanceRef.current && segments.length > 0 && trailBases) {
        drawSegments(mapInstanceRef.current, segments, trailBases)
      }
  }, [segments]);

    return (
        <div className={styles.mapContainer}>
            <div
                id={`map-${areaShortName}`}
                ref={mapRef}
                className={styles.mapContainer}
            ></div>
            {error && <p>{error}</p>}
        </div>
    );
};

export default TrailAreaMap;
