import React from "react";
import { Link } from "react-router-dom";
import "../styles/Navbar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="nav-left">
        <div className="logo">
        <a href="https://www.ibm.com" target="_blank" rel="noopener noreferrer" className="logo">
          <img src="/ibm.png" alt="IBM Logo" />
        </a>
        </div>
        <div className="separator"></div>
        <Link
          to="/"
          className="home-link"
          style={{ textDecoration: "none", color: "inherit" }}
        >
          Home
        </Link>
        <Link
          to="/about"
          className="about-link"
          style={{ textDecoration: "none", color: "inherit" }}
        >
          About
        </Link>
        <Link
          to="/upload"
          className="upload-link"
          style={{ textDecoration: "none", color: "inherit" }}
        >
          Code Review
        </Link>
        <Link
          to="/how_to_use"
          className="how_to_use-link"
          style={{ textDecoration: "none", color: "inherit" }}
        >
          How_To_Use
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
