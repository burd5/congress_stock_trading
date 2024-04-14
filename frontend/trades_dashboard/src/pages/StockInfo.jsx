import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { format } from 'date-fns';
import Plotly from 'plotly.js-dist-min';

const StockInfoPage = () => {
    const { politician_id, type, ticker, date, amount } = useParams();
    const [stockData, setStockData] = useState(null);
    const [stockName, setStockName] = useState(null);
    const [politicianData, setPoliticianData] = useState(null);
    const [performancePercentage, setPerformancePercentage] = useState(null);
    const [loading, setLoading] = useState(true);
    const chartRef = React.useRef(null);

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

    const purchaseDateFormatted = format(new Date(date), 'MM/dd/yyyy');

    const getTypeLabel = (type) => {
        switch (type) {
            case 'Sale':
                return 'Sold';
            case 'Purchase':
                return 'Purchased';
            case 'Exchange':
                return 'Exchanged';
            case 'Sale (partial)':
                return 'Sold Partial';
            case 'Sale (full)':
                return 'Sold';
            default:
                return type; // Return the original type if no match is found
        }
    };

    useEffect(() => {
        if (!stockData) return;

        // Prepare data for plotting
        const data = Object.entries(stockData).map(([date, values]) => ({
            date: format(new Date(date), 'MM/dd/yyyy'),
            close: parseFloat(values['Close']),
        }));

        // Get purchase date close price
        const purchaseDateIndex = data.findIndex((d) => d.date === purchaseDateFormatted);
        const purchaseClosePrice = data[purchaseDateIndex]?.close;

        // Split data into before and after purchase date
        const beforeData = data.slice(0, purchaseDateIndex + 1);
        const afterData = data.slice(purchaseDateIndex);

        // Determine line color for the afterData
        const afterColor = afterData[afterData.length - 1].close > purchaseClosePrice ? '#39FF14' : '#FF0000';

        // Create traces for before and after purchase date
        const beforeTrace = {
            x: beforeData.map((d) => d.date),
            y: beforeData.map((d) => d.close),
            mode: 'lines',
            line: {
                color: '#B0B0B0',
                shape: 'spline',
            },
            name: 'Before Transaction',
        };

        const afterTrace = {
            x: afterData.map((d) => d.date),
            y: afterData.map((d) => d.close),
            mode: 'lines',
            line: {
                color: afterColor,
                shape: 'spline',
            },
            name: 'After Transaction',
        };

        // Layout settings
        const layout = {
            title: {
                text: `${ticker} Stock Price History`,
                font: {
                    color: 'black',
                },
            },
            xaxis: {
                title: {
                    text: 'Date',
                    font: {
                        color: 'black',
                    },
                },
                showgrid: false,
                showticklabels: true,
                tickfont: {
                    color: 'black',
                },
                tickvals: data.map((d, i) => {
                    // Return index values every 30 days (or desired frequency)
                    if (i >= 20 && (i - 20) % 30 === 0) {
                        return i;
                    }
                    return null;
                }).filter((v) => v !== null),
                ticktext: data.map((d, i) => {
                    // Return formatted dates every 30 days
                    if (i >= 20 && (i - 20) % 30 === 0) {
                        return format(new Date(d.date), 'MMM yyyy');
                    }
                    return null;
                }).filter((v) => v !== null),
            },
            yaxis: {
                title: {
                    text: 'Close Price',
                    font: {
                        color: 'black',
                    },
                },
                showgrid: false,
                tickfont: {
                    color: 'black',
                },
            },
            paper_bgcolor: 'white',
            plot_bgcolor: 'white',
            hovermode: 'closest',
            hoverlabel: {
                bgcolor: 'white',
                font: {
                    color: 'black',
                },
            },
            showlegend: true,
            legend: {
                x: 0.85,
                y: 1.3,
                bgcolor: 'rgba(255, 255, 255, 0.9)',
                bordercolor: 'black',
                borderwidth: 1,
                font: {
                    color: 'black',
                },
            },
        };

        // Simplify tooltips to only show date and price
        beforeTrace.hovertemplate = 'Date: %{x}<br>Close Price: $%{y:.2f}<extra></extra>';
        afterTrace.hovertemplate = 'Date: %{x}<br>Close Price: $%{y:.2f}<extra></extra>';

        // Plot the data
        Plotly.newPlot(chartRef.current, [beforeTrace, afterTrace], layout, { displayModeBar: false });
    }, [stockData]);

    return (
        <div style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'flex-start',
            width: '100%',
            padding: '20px',
            boxSizing: 'border-box',
        }}>
            {/* Title card */}
            <div style={{
                width: '25%',
                padding: '15px',
                borderRadius: '8px',
                backgroundColor: 'white',
                color: 'black',
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.15)',
                textAlign: 'center',
                height: '500px', // Set the height to match the chart card
                marginRight: '10px',
            }}>
                {/* Displaying politician data */}
                {politicianData && (
                    <>
                        <h2>{politicianData[1]}</h2>
                        <img
                            src={politicianData[6]}
                            alt={`${politicianData[1]} Photo`}
                            className="politician-image"
                        />
                        <p>{`${politicianData[2]} - ${politicianData[4]} - ${politicianData[5]}`}</p>
                        <h4>{`${stockName[2]} (${stockName[1]})`}</h4>
                    </>
                )}
                <p>{getTypeLabel(type)} {amount} on {date}</p>

                {/* Displaying performance percentage with corresponding arrow */}
                {performancePercentage !== null && (
                    <p style={{ marginTop: '10px' }}> 
                        {performancePercentage >= 0 ? (
                            <span style={{ color: 'green' }}>
                                &#x2191; {`${performancePercentage.toFixed(2)}%`}
                            </span>
                        ) : (
                            <span style={{ color: 'red' }}>
                                &#x2193; {`${performancePercentage.toFixed(2)}%`}
                            </span>
                        )}
                    </p>
                )}
            </div>

            {/* Chart card */}
            <div style={{
                width: '75%',
                padding: '15px',
                borderRadius: '8px',
                backgroundColor: 'white',
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.15)',
                height: '500px', // Set height explicitly
            }}>
                {loading ? (
                    <div className="loading-overlay">
                        <div className="loading-circle"></div>
                    </div>
                ) : (
                    <div ref={chartRef} style={{ height: '100%', width: '100%' }} />
                )}
            </div>
        </div>
    );
};

export default StockInfoPage;
