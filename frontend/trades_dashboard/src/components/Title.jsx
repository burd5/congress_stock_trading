import React from 'react';

const TitleCard = ({ politicianData, stockName, type, amount, date, performancePercentage, getTypeLabel }) => {
    const getPoliticianPartyColor = (party) => {
        switch (party) {
            case 'Democrat':
                return '#0047AB';
            case 'Republican':
                return '#C41E3A';
            case 'Independent':
                return 'purple';
            default:
                return 'black';
        }
    };

    const partyColor = politicianData ? getPoliticianPartyColor(politicianData[4]) : 'black';

    // Check if all necessary data is available
    const allDataAvailable = politicianData && stockName && type && amount && date && performancePercentage !== null;

    return (
        // Conditionally render the entire card based on data availability
        allDataAvailable && (
            <div className="title-card" style={{ boxShadow: `0 0 15px ${partyColor}` }}>
                <>
                    <h2 style={{ marginTop: '0px' }}>{politicianData[1]}</h2>
                    <img
                        src={politicianData[6]}
                        alt={`${politicianData[1]} Photo`}
                        className="politician-image"
                    />
                    <p>{`${politicianData[2]} - ${politicianData[4]} - ${politicianData[5]}`}</p>
                    <h4>Stock</h4>
                    <p>{`${stockName[2]} (${stockName[1]})`}</p>
                    <h4>Date</h4>
                    <p>
                        {getTypeLabel(type)} Stock on {date}
                    </p>
                    <h4>Amount</h4>
                    <p>{amount}</p>
                    <h4>Performance Since Trade</h4>
                    <p>
                        {performancePercentage >= 0 ? (
                            <span style={{ color: 'green' }}>
                                &#x2191; {performancePercentage.toFixed(2)}%
                            </span>
                        ) : (
                            <span style={{ color: 'red' }}>
                                &#x2193; {performancePercentage.toFixed(2)}%
                            </span>
                        )}
                    </p>
                </>
            </div>
        )
    );
};

export default TitleCard;
