import * as React from 'react';
import { LocalRider } from '../types/TrailArea';
import { FaInstagram } from 'react-icons/fa';
import styles from './TrailAreaContacts.module.css'

interface TrailAreaContactsProps {
    instagram: string[];
    localRiders: LocalRider[]
}

const TrailAreaContacts: React.FC<TrailAreaContactsProps> = ({ instagram, localRiders }) => {
    return (
        <div>
            <h2>Contacts</h2>
            <div>
                <ul className={styles.list}>
                    {instagram.map((accountUrl, index) => (
                        <li key={index}>
                            <a
                                href={accountUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                                className={styles.iconLink}
                            >
                                <FaInstagram className={styles.icon}/> Trail Area Page
                            </a>
                        </li>
                    ))}
                </ul>
            </div>
            <div>
                <h3>Local Riders</h3>
                <ul className={styles.list}>
                    {localRiders.map((rider) => (
                        <li key={rider.strava_id}>
                            <a
                                href={rider.strava_id}
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                {rider.name}
                            </a>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default TrailAreaContacts;
