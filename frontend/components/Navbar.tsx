import React from "react";
import Link from "next/link";
import "../styles/Navbar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="nav-left">
        <div className="logo">
          <a
            href="https://www.ibm.com"
            target="_blank"
            rel="noopener noreferrer"
            className="logo"
          >
            <img src="/ibm.png" alt="IBM Logo" />
          </a>
        </div>
        <div className="separator"></div>
        <Link
          href="/"
          className="home-link"
          style={{ textDecoration: "none", color: "inherit" }}
        >
          Home
        </Link>
        <Link
          href="/about"
          className="about-link"
          style={{ textDecoration: "none", color: "inherit" }}
        >
          About
        </Link>
        <Link
          href="/security-analysis"
          className="security-analysis-link"
          style={{ textDecoration: "none", color: "inherit" }}
        >
          Security Analysis
        </Link>
        <Link
          href="/how-to-use"
          className="how-to-use-link"
          style={{ textDecoration: "none", color: "inherit" }}
        >
          How To Use
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;