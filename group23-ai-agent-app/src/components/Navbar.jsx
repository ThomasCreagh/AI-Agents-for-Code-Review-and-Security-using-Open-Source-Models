import React from "react";
import { Link } from "react-router-dom";
import "../styles/Navbar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="nav-left">
        <div className="logo">
          <img src="/ibm.png" alt="IBM Logo" />
        </div>
        <div className="separator"></div>
        <Link to="/about" className="about-link" style={{ textDecoration: "none", color: "inherit" }}>
          About
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
