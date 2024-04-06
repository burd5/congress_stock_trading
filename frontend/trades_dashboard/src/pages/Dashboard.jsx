import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactTable from 'react-table-6';
import 'react-table-6/react-table.css';
import '../styles/dashboard.css';

const Dashboard = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true); 

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/trades');
        const sortedData = response.data.sort((a, b) => {
          const dateA = new Date(a.transaction_date).getTime();
          const dateB = new Date(b.transaction_date).getTime();
          return dateB - dateA;
        });
        setData(sortedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false); 
      }
    };

    fetchData();
  }, []);

  const columns = [
    { Header: 'Politician Name', accessor: 'politician_name' },
    { Header: 'Stock Ticker', accessor: 'stock_ticker' },
    { Header: 'Stock Information', accessor: 'stock_information' },
    { Header: 'Transaction Type', accessor: 'purchased_or_sold'},
    { Header: 'Transaction Date', accessor: 'transaction_date', sortMethod: (a, b) => {
      const dateA = new Date(a).getTime();
      const dateB = new Date(b).getTime();
      return dateA - dateB;
    }},
    { Header: 'Amount', accessor: 'amount' },
  ];

  return (
    <div className="container">
      <div className="table-container">
        {loading && <div className="loader" />}
        <ReactTable
          data={data}
          columns={columns}
          defaultPageSize={20}
          className="-striped -highlight"
          style={{ visibility: loading ? 'hidden' : 'visible' }}
        />
      </div>
    </div>
  );
};

export default Dashboard;
