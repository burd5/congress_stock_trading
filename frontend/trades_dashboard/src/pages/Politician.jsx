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
                    };
                    setPoliticianData(formattedData);
                    console.log('Fetched politician data:', formattedData);
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
                <div className="card-container">  {/* Add a container with card styles */}
                    {/* Image Placeholder */}
                    <img src="#" alt="Politician" className="politician-image" />  {/* Replace "#" with the actual image URL */}
                    
                    {/* Politician Information */}
                    <div className="politician-info">
                        <h2>{politicianData ? politicianData.name : id}</h2>
                        {politicianData ? (
                            <div className="politician-details">
                                {/* Stack Office, State, and Party */}
                                <p><strong>Office:</strong> {politicianData.office}</p>
                                <p><strong>State:</strong> {politicianData.state}</p>
                                <p><strong>Party:</strong> {politicianData.political_party}</p>
                            </div>
                        ) : (
                            <div>Failed to fetch politician data.</div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Politician;
