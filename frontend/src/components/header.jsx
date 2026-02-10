import React from 'react';
import logo from '../assets/logo2.png';


const Header = () => {
  return (
    <header className="app-header">
      
      {/* left box: Logo */}
      <div className="header-brand">
        <img src={logo} alt="Primera Logo" className="app-logo" />
      </div>
      
      {/* right box: Navi  Menu */}
      <div className="header-nav">
        <nav className="nav-links">
          
          <button className="nav-btn active">Home</button>
          <button className="nav-btn">Previous Runs</button>
          <button className="nav-btn">Help</button>
          <button className="nav-btn">About</button>
          <button className="nav-btn">Contact</button>
        </nav>
      </div>

    </header>
  );
};

export default Header;