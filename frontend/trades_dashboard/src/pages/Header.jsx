import React from 'react';

// Header component
const Header = () => {
  return (
    <div className="header">
      <div className="header-left">
        {/* Logo component */}
        <img src="logo.png" alt="Logo" className="logo" />
        {/* Title */}
        <h1>Congress Trade Transactions</h1>
      </div>
      <div className="header-right">
        {/* Search bar component */}
        <input type="text" placeholder="Search..." className="search-bar" />
      </div>
    </div>
  );
};

export default Header;
