import React, { useEffect, useRef, useState } from 'react';
import Plotly from 'plotly.js-dist-min';
import { format, parse } from 'date-fns';

const ChartCard = ({ stockData, ticker, purchaseDateFormatted, loading }) => {
    const chartRef = useRef(null);
    const [afterColor, setAfterColor] = useState('#FFFFFF');

    useEffect(() => {
        if (!stockData) return;
        console.log(stockData)
        // Prepare data for plotting
        const data = Object.entries(stockData).map(([date, values]) => ({
            date: format(parse(date, 'yyyy-MM-dd', new Date()), 'MM/dd/yyyy'),
            close: parseFloat(values['Close']),
        }));        
        

        // Get purchase date close price
        const purchaseDateIndex = data.findIndex((d) => d.date === purchaseDateFormatted);
        console.log(purchaseDateIndex)
        const purchaseClosePrice = data[purchaseDateIndex]?.close;
        console.log(purchaseClosePrice)

        // Split data into before and after purchase date
        const beforeData = data.slice(0, purchaseDateIndex + 1);
        const afterData = data.slice(purchaseDateIndex);

        // Determine line color for the afterData
        const afterColor = afterData[afterData.length - 1].close > purchaseClosePrice ? '#009E60' : '#FF0000';
        setAfterColor(afterColor);

        // Create traces for before and after purchase date
        const beforeTrace = {
            x: beforeData.map((d) => d.date),
            y: beforeData.map((d) => d.close),
            mode: 'lines',
            line: {
                color: '#3b3b3b',
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
        <div className="chart-card" style={{boxShadow: `0 0 8px ${afterColor}` }}>
            <div ref={chartRef} style={{ height: '100%', width: '100%' }} />
        </div>
    );
};

export default ChartCard;
