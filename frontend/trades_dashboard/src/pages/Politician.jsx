import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import '../styles/politician.css'; // Import the CSS file for styling

const Politician = () => {
    const { id } = useParams();
    const [politicianData, setPoliticianData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const response = await axios.get(`http://127.0.0.1:5000/politicians/${id}`);
                if (response.status === 200) {
                    const data = response.data;
                    const formattedData = {
                        id: data[0],
                        name: data[1],
                        office: data[2],
                        state: data[3],
                        political_party: data[4],
                        image: data[6]
                    };
                    setPoliticianData(formattedData);
                } else {
                    console.error('Failed to fetch data');
                }
            } catch (error) {
                console.error('Error fetching politician data:', error);
            }
            setLoading(false);
        };

        fetchData();
    }, [id]);

    return (
        <div className="page-container">
            {loading ? (
                <div className="loading-overlay">
                    <div className="loading-circle"></div>
                </div>
            ) : (
                <div className="card-container">
                    {/* Politician Information */}
                    <div className="politician-info">
                        {politicianData && (
                            <div className="politician-header">
                                {/* Politician Name */}
                                <h2>{politicianData.name}</h2>
                                {/* Politician Image */}
                                <img
                                    src={politicianData.image}
                                    alt={`${politicianData.name} Photo`}
                                    className="politician-image"
                                />
                            </div>
                        )}
                        {/* Politician Details */}
                        {politicianData && (
                            <div className="politician-details">
                                {/* Format: "{office} {political_party}/{state}" */}
                                <p>{`${politicianData.office} - ${politicianData.political_party} - ${politicianData.state}`}</p>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Politician;
