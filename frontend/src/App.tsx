import { useEffect, useState } from 'react';
import './App.css';
import { fetchTrailAreas } from './api';
import { TrailArea } from './types/TrailArea';

function App() {
    const [count, setCount] = useState(0);
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
        <>
            <h1>Vite + React</h1>
            <div>
                <h2>Trail Areas</h2>
                {error && <p>{error}</p>}
                <ul>
                    {trailAreas.map((area) => (
                        <li key={area.name}>
                            <h3>{area.name}</h3>
                            <p>Instagram: {area.instagram.join(', ')}</p>
                        </li>
                    ))}
                </ul>
            </div>
        </>
    );
}

export default App;
