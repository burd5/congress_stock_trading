import React from 'react';
import logo from '../images/flag_circle.jpeg';

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

export default Header;
