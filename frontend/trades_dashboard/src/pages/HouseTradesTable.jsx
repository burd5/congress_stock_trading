import React, { useState } from 'react';

const HouseTradesTable = ({ trades }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [recordsPerPage] = useState(20);

  // Get current records
  const indexOfLastRecord = currentPage * recordsPerPage;
  const indexOfFirstRecord = indexOfLastRecord - recordsPerPage;
  const currentRecords = trades.slice(indexOfFirstRecord, indexOfLastRecord);

  // Change page
  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  // Sort by column
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'ascending' });

  const requestSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const sortedRecords = () => {
    let sortableRecords = [...currentRecords];
    if (sortConfig.key !== null) {
      sortableRecords.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableRecords;
  };

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th onClick={() => requestSort('id')}>ID</th>
            <th onClick={() => requestSort('politician_name')}>Politician Name</th>
            <th onClick={() => requestSort('stock_ticker')}>Stock Ticker</th>
            <th onClick={() => requestSort('stock_information')}>Stock Information</th>
            <th onClick={() => requestSort('purchased_or_sold')}>Purchased or Sold</th>
            <th onClick={() => requestSort('transaction_date')}>Transaction Date</th>
            <th onClick={() => requestSort('amount')}>Amount</th>
          </tr>
        </thead>
        <tbody>
          {sortedRecords().map((trade) => (
            <tr key={trade.id}>
              <td>{trade.id}</td>
              <td>{trade.politician_name}</td>
              <td>{trade.stock_ticker}</td>
              <td>{trade.stock_information}</td>
              <td>{trade.purchased_or_sold}</td>
              <td>{trade.transaction_date}</td>
              <td>{trade.amount}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <Pagination
        recordsPerPage={recordsPerPage}
        totalRecords={trades.length}
        paginate={paginate}
        currentPage={currentPage}
      />
    </div>
  );
};

export default HouseTradesTable;
