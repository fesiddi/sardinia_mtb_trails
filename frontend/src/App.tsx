import { useEffect, useState } from 'react';
import styles from './App.module.css';
import { fetchTrailAreas } from './api';
import { TrailArea } from './types/TrailArea';
import TrailAreaDescription from './components/TrailAreaDescription.tsx';
import TrailAreaContacts from './components/TrailAreaContacts.tsx';
import TrailAreaMap from './components/TrailAreaMap.tsx';


function App() {
    const [trailAreas, setTrailAreas] = useState<TrailArea[]>([]);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const getTrailAreas = async () => {
            try {
                const data = await fetchTrailAreas();
                setTrailAreas(data);
            } catch (error) {
                setError('Failed to fetch trail areas');
            }
        };

        getTrailAreas();
    }, []);

    return (
        <div className={styles.container}>
            <h1>Trail Areas</h1>
            <div className={styles.areasList}>
                {trailAreas.map((area) => (
                    <div key={area.name} className={styles.area}>
                        <TrailAreaDescription
                            name={area.name}
                            description={area.description}
                        />
                        <TrailAreaMap areaShortName={area.s_name} trailBases={area.trail_bases} />
                        <TrailAreaContacts
                            instagram={area.instagram}
                            localRiders={area.local_riders}
                        />
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App;
