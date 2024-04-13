import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import ReactTable from 'react-table-6';
import 'react-table-6/react-table.css';
import '../styles/dashboard.css';
import logo from '../images/logo.png'
import { format } from 'date-fns';

// Header component
const Header = () => {
    return (
        <div className="header">
            <div className="header-left">
                <img src={logo} alt="Logo" className="logo" />
                <h1>Congress Trades</h1>
            </div>
            <div className="header-right">
                {/* Search bar component */}
                <input type="text" placeholder="Search..." className="search-bar" />
            </div>
        </div>
    );
};

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
                    political_party: row[8] // Assuming political party is at index 8 in the row data
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

    const columns = [
        {
            Header: 'Politician Name',
            accessor: 'politician_name',
            Cell: row => (
                <Link
                    to={`/politicians/${row.original.politician_id}`}
                    className="table-cell"
                    style={{
                        color: getPoliticianNameColor(row.original.political_party),
                        display: 'block',
                        textAlign: 'center',
                        textDecoration: 'none'
                    }}
                >
                    {row.value}
                </Link>
            )
        },
        {
            Header: 'Stock Ticker',
            accessor: 'stock_ticker',
            Cell: row => (
                row.value !== '--' ? (
                    <Link
                        to={`/stock-info/${row.original.politician_name}/${row.original.purchased_or_sold}/${row.value}/${encodeURIComponent(row.original.transaction_date)}`}
                        style={{ color: 'black', display: 'block', textAlign: 'center' }}
                        className="table-cell"
                    >
                        {row.value}
                    </Link>
                ) : (
                    <span className="table-cell">{row.value}</span>
                )
            )
        },
        { Header: 'Stock Information', accessor: 'stock_information', className: "table-cell" },
        { Header: 'Transaction Type', accessor: 'purchased_or_sold', className: "table-cell" },
        {
            Header: 'Transaction Date',
            accessor: 'transaction_date',
            className: "table-cell"
        },
        {
            Header: 'Amount',
            accessor: 'amount',
            className: "table-cell"
        },
    ];

    const getPoliticianNameColor = (party) => {
        switch (party) {
            case 'Democrat':
                return 'blue';
            case 'Republican':
                return 'red';
            case 'Independent':
                return 'purple';
            default:
                return 'black';
        }
    };

    return (
        <div>
            {/* Header component */}
            <Header />
            {/* Dashboard container */}
            <div className="dashboard-container">
                {/* Conditional rendering of loading spinner */}
                {loading && (
                    <div className="loading-overlay">
                        <div className="loading-circle"></div>
                    </div>
                )}
                {/* ReactTable component */}
                {!loading && (
                    <ReactTable
                        data={data}
                        columns={columns}
                        defaultPageSize={10}
                        className="-striped -highlight"
                    />
                )}
            </div>
        </div>
    );
};

export default Dashboard;
