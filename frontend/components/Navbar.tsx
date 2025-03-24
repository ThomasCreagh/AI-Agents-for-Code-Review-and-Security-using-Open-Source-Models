import Link from "next/link"
import "../styles/Navbar.css"

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
        <Link href="/" className="home-link" style={{ textDecoration: "none", color: "inherit" }}>
          Home
        </Link>
        <Link href="/about" className="about-link" style={{ textDecoration: "none", color: "inherit" }}>
          About
        </Link>
        <Link
          href="/security-analysis"
          className="security-analysis-link"
          style={{ textDecoration: "none", color: "inherit" }}
        >
          Security Analysis
        </Link>
        <Link href="/how-to-use" className="how-to-use-link" style={{ textDecoration: "none", color: "inherit" }}>
          How To Use
        </Link>
      </div>
      <div className="nav-right">
        <Link href="/login" className="login-link">
          <button className="login-button">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
              <polyline points="10 17 15 12 10 7"></polyline>
              <line x1="15" y1="12" x2="3" y2="12"></line>
            </svg>
            Login
          </button>
        </Link>
      </div>
    </nav>
  )
}

export default Navbar

