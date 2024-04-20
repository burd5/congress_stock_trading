import React from 'react';
import { Link } from 'react-router-dom';
import ReactTable from 'react-table-6';
import 'react-table-6/react-table.css';
import { format } from 'date-fns';

const DataTable = ({ data, loading }) => {
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
                        to={`/stock-info/${row.original.politician_id}/${row.original.purchased_or_sold}/${row.value}/${encodeURIComponent(row.original.transaction_date)}/${row.original.amount}`}
                        style={{ color: 'black', display: 'block', textAlign: 'center' }}
                        className="table-cell"
                    >
                        {row.value}
                    </Link>
                ) : (
                    <span style={{ color: 'black', display: 'block', textAlign: 'center' }} className="table-cell">{row.value}</span>
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
        !loading && (
            <ReactTable
                data={data}
                columns={columns}
                defaultPageSize={10}
                className="-striped -highlight"
            />
        )
    );
};

export default DataTable;
