import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { format } from 'date-fns';
import Plotly from 'plotly.js-dist-min';

const StockInfoPage = () => {
    const { name, type, ticker, date } = useParams();
    const [stockData, setStockData] = useState(null);
    const [loading, setLoading] = useState(true);
    const chartRef = React.useRef(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await axios.get('http://127.0.0.1:5000/stock-info', {
                    params: {
                        name,
                        type,
                        ticker,
                        date: encodeURIComponent(date),
                    },
                });

                if (response.status === 200) {
                    setStockData(response.data);
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
    }, [name, type, ticker, date]);

    const purchaseDateFormatted = format(new Date(date), 'MM/dd/yyyy');

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
            name: 'Before Transaction', // Update legend name
        };

        const afterTrace = {
            x: afterData.map((d) => d.date),
            y: afterData.map((d) => d.close),
            mode: 'lines',
            line: {
                color: afterColor,
                shape: 'spline',
            },
            name: 'After Transaction', // Update legend name
        };

        // Create layout
        const layout = {
          title: {
              text: `${ticker} Stock Prices`,
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
                // Start from 20 days in, then show ticks every 30 days (or whatever frequency you want)
                if (i >= 20 && (i - 20) % 30 === 0) {
                    return i;
                }
                return null;
            }).filter((v) => v !== null),
            ticktext: data.map((d, i) => {
                // Start from 20 days in, then format dates every 30 days
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
              bgcolor: 'white', // Set tooltip background color to white
              font: {
                  color: 'black', // Set tooltip text color to black
              },
          },
          showlegend: true,
          legend: {
              x: 0.75, // Set x-position of the legend (0 to 1, from left to right)
              y: 1.3, // Set y-position of the legend (0 to 1, from bottom to top)
              bgcolor: 'rgba(255, 255, 255, 0.9)',
              bordercolor: 'black',
              borderwidth: 1,
              font: {
                  color: 'black',
              },
          }
      };
      
        // Simplify tooltips to only show date and price
        beforeTrace.hovertemplate = 'Date: %{x}<br>Close Price: $%{y:.2f}<extra></extra>';
        afterTrace.hovertemplate = 'Date: %{x}<br>Close Price: $%{y:.2f}<extra></extra>';

        // Plot the data
        Plotly.newPlot(chartRef.current, [beforeTrace, afterTrace], layout, { displayModeBar: false });
    }, [stockData]);

    return (
        <div>
            {/* Politician card */}
            <div style={{
                width: '50%',
                margin: 'auto',
                padding: '15px',
                borderRadius: '8px',
                backgroundColor: 'white', // Set card background color to white
                color: 'black', // Set text color to black
                textAlign: 'center',
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', // Add a light silhouette effect
            }}>
                <h2>{name}</h2>
                <h4>{ticker} | {type}</h4>
                <p>{date}</p>
            </div>

            {/* Graph card */}
            <div style={{
                width: '50%',
                margin: 'auto',
                marginTop: '20px', // Add space between cards
                padding: '15px',
                borderRadius: '8px',
                backgroundColor: 'white', // Set card background color to white
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', // Add a light silhouette effect
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
