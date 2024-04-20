import { useState, useEffect } from 'react';
import axios from 'axios';

export function useStockData(politician_id, type, ticker, date, amount) {
    const [stockData, setStockData] = useState(null);
    const [politicianData, setPoliticianData] = useState(null);
    const [stockName, setStockName] = useState(null);
    const [performancePercentage, setPerformancePercentage] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await axios.get('http://127.0.0.1:5000/stock-info', {
                    params: {
                        politician_id,
                        type,
                        ticker,
                        date: encodeURIComponent(date),
                        amount,
                    },
                });

                if (response.status === 200) {
                    setStockData(response.data[0]);
                    setPoliticianData(response.data[1]);
                    setStockName(response.data[2]);
                    setPerformancePercentage(response.data[3]);
                    setLoading(false);
                } else {
                    throw new Error('Failed to fetch data');
                }
            } catch (error) {
                console.error('Error fetching stock data:', error);
                setLoading(false);
            }
        };

        fetchData();
    }, [politician_id, type, ticker, date, amount]);

    return { stockData, politicianData, stockName, performancePercentage, loading };
}
