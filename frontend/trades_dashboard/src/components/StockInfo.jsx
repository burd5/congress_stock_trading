import React from 'react';
import { useParams } from 'react-router-dom';
import { format } from 'date-fns';
import { useStockData } from './StockHook';
import TitleCard from './Title';
import ChartCard from './StockChart';
import LoadingOverlay from './LoadingOverlay'; // Import the LoadingOverlay component
import '../styles/stockinfo.css';

const StockInfoPage = () => {
    const { politician_id, type, ticker, date, amount } = useParams();
    const {
        stockData,
        politicianData,
        stockName,
        performancePercentage,
        loading,
    } = useStockData(politician_id, type, ticker, date, amount);

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
            case 'Sale (Partial)':
                return 'Sold Partial';
            case 'Sale (full)':
                return 'Sold';
            case 'Sale (Full)':
                return 'Sold';
            default:
                return type;
        }
    };

    return (
        <div className="stock-info-container">

            {/* Display loading overlay if data is loading */}
            {loading && <LoadingOverlay />}

            {/* Only render components if data is not loading */}
            {!loading && (
                <>
                    {/* TitleCard component */}
                    <TitleCard
                        politicianData={politicianData}
                        stockName={stockName}
                        type={type}
                        amount={amount}
                        date={date}
                        performancePercentage={performancePercentage}
                        getTypeLabel={getTypeLabel}
                    />

                    {/* ChartCard component */}
                    <ChartCard
                        stockData={stockData}
                        ticker={ticker}
                        purchaseDateFormatted={purchaseDateFormatted}
                        loading={loading}
                    />
                </>
            )}
        </div>
    );
};

export default StockInfoPage;
