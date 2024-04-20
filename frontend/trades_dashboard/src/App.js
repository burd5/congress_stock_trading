import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import StockInfo from './components/StockInfo';
import Politician from './components/Politician';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/stock-info/:politician_id/:type/:ticker/:date/:amount" element={<StockInfo />} />
        <Route path="/politicians/:id" element={<Politician />} />
      </Routes>
    </Router>
  );
};

export default App;
