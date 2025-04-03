"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { supabase } from "@/src/services/supabaseClient";
import "../styles/Navbar.css";
import Image from "next/image";

const Navbar = () => {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userEmail, setUserEmail] = useState("");

  useEffect(() => {
    const checkSession = async () => {
      const { data } = await supabase.auth.getSession();
      console.log("Logged in user:", data.session?.user);
      if (data.session) {
        setIsLoggedIn(true);
        const fullName = data.session.user.user_metadata?.full_name || "";
        setUserEmail(fullName);
      } else {
        setIsLoggedIn(false);
        setUserEmail("");
      }
    };

    checkSession();

    const { data: listener } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        if (session) {
          setIsLoggedIn(true);
          const fullName = session.user.user_metadata?.full_name || "";
          setUserEmail(fullName);
        } else {
          setIsLoggedIn(false);
          setUserEmail("");
        }
      },
    );

    return () => {
      listener?.subscription.unsubscribe();
    };
  }, []);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    router.push("/login");
  };

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
            <Image src="/ibm.png" alt="IBM Logo" />
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
      <div className="nav-right">
        {isLoggedIn ? (
          <>
            <div
              className="user-info"
              style={{ marginRight: "1rem", color: "#393939" }}
            >
              Logged in as: <strong>{userEmail}</strong>
            </div>
            <button className="login-button" onClick={handleLogout}>
              Logout
            </button>
          </>
        ) : (
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
        )}
      </div>
    </nav>
  );
};

export default Navbar;
