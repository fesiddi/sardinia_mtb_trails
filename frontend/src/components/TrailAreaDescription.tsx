import * as React from 'react';

interface TrailAreaDescriptionProps {
    name: string;
    description: string;
}

const TrailAreaDescription: React.FC<TrailAreaDescriptionProps> = ({name,
    description,
}) => {
    return (
        <div>
            <h2>{name} Trail Area</h2>
            <p>{description}</p>
        </div>
    );
};

export default TrailAreaDescription;
