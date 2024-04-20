import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { format } from 'date-fns';
import Header from './Header';
import DataTable from './StocksTable';
import LoadingOverlay from './LoadingOverlay'; // Import the LoadingOverlay component
import '../styles/dashboard.css';

const Dashboard = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await axios.get('http://127.0.0.1:5000/trades');
                const transformedData = response.data.map(row => ({
                    politician_name: row[0],
                    politician_id: row[1],
                    stock_ticker: row[2],
                    stock_information: row[3],
                    purchased_or_sold: row[4],
                    transaction_date: format(new Date(row[5]), 'MM/dd/yyyy'),
                    amount: row[6],
                    political_party: row[8]
                }));
                setData(transformedData);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching data:', error);
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    return (
        <div>
            {/* Display loading overlay if data is loading */}
            {loading && <LoadingOverlay />}

            {/* Render content only if data is not loading */}
            {!loading && (
                <>
                    <Header />
                    <div className="dashboard-container">
                        <div className="data-table-container">
                            <DataTable data={data} loading={loading} />
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};

export default Dashboard;
