"use client";
import React, { useEffect, useState } from "react";
import { Globe, Linkedin, ArrowUp } from "lucide-react";

const Footer: React.FC = () => {
  return (
    <>
      <footer className="w-full bg-white/80 backdrop-blur-md border-t border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-6 flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-gray-700">
          {/* Left: Info */}
          <div className="text-center sm:text-left">
            <p className="font-semibold text-[#0f62fe] tracking-tight">
              KeySentinel 2025
            </p>
            <p className="text-xs text-gray-500 mt-1">
              Built by TCD Software Engineering Group 23
            </p>
          </div>

          {/* Right: Links */}
          <div className="flex flex-wrap gap-5 justify-center sm:justify-end">
            <FooterLink
              href="https://www.instagram.com/keysentinel"
              label="Instagram"
              icon={<InstagramLucideGradientIcon />}
            />
            <FooterLink
              href="https://gitlab.scss.tcd.ie/sweng25_group23_CodeReviewSecurity"
              label="GitLab"
              icon={<GitLabLucideIcon />}
            />
            <FooterLink
              href="https://keysentinel.vercel.app"
              label="Live Site"
              icon={
                <Globe className="w-4 h-4 text-gray-500 group-hover:text-[#0f62fe]" />
              }
            />
            <FooterLink
              href="https://www.linkedin.com/company/tcd-scss-sweng/"
              label="LinkedIn"
              icon={
                <Linkedin className="w-4 h-4 text-gray-500 group-hover:text-[#0f62fe]" />
              }
            />
          </div>
        </div>
      </footer>

      {/* Scroll to Top */}
      <ScrollToTopButton />
    </>
  );
};

interface FooterLinkProps {
  href: string;
  label: string;
  icon: React.ReactNode;
}

const FooterLink: React.FC<FooterLinkProps> = ({ href, label, icon }) => (
  <a
    href={href}
    target="_blank"
    rel="noopener noreferrer"
    className="group flex items-center gap-1 text-gray-600 hover:text-[#0f62fe] transition-all relative px-1"
  >
    <span className="transition-transform group-hover:scale-110">{icon}</span>
    <span className="relative after:absolute after:left-0 after:bottom-[-2px] after:h-[2px] after:w-0 group-hover:after:w-full after:bg-[#0f62fe] after:transition-all after:duration-300">
      {label}
    </span>
  </a>
);

const InstagramLucideGradientIcon: React.FC = () => (
  <svg
    className="w-4 h-4 transition-all duration-300 group-hover:scale-110"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <defs>
      <linearGradient id="lucide-insta-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#feda75" />
        <stop offset="30%" stopColor="#fa7e1e" />
        <stop offset="60%" stopColor="#d62976" />
        <stop offset="100%" stopColor="#962fbf" />
      </linearGradient>
    </defs>
    <g className="text-gray-500 group-hover:[stroke:url(#lucide-insta-gradient)]">
      <rect x="2" y="2" width="20" height="20" rx="5" ry="5" />
      <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" />
      <line x1="17.5" y1="6.5" x2="17.51" y2="6.5" />
    </g>
  </svg>
);

const GitLabLucideIcon: React.FC = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="20"
    height="20"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className="w-4 h-4 text-gray-500 group-hover:text-[#fc6d26] transition-colors"
    viewBox="0 0 24 24"
  >
    <path d="M22.65 14.39L12 22.13 1.35 14.39a.84.84 0 0 1-.3-.94l1.22-3.78 2.44-7.51A.42.42 0 0 1 4.82 2a.43.43 0 0 1 .58 0 .42.42 0 0 1 .11.18l2.44 7.49h8.1l2.44-7.51A.42.42 0 0 1 18.6 2a.43.43 0 0 1 .58 0 .42.42 0 0 1 .11.18l2.44 7.49L23 13.45a.84.84 0 0 1-.35.94z" />
  </svg>
);

const ScrollToTopButton: React.FC = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const toggleVisibility = () => {
      setIsVisible(window.scrollY > 100);
    };

    window.addEventListener("scroll", toggleVisibility);
    return () => window.removeEventListener("scroll", toggleVisibility);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <button
      onClick={scrollToTop}
      className={`fixed bottom-6 right-6 z-50 p-3 rounded-full shadow-md transition-opacity duration-300 bg-[#0f62fe] text-white hover:bg-[#0353e9] ${
        isVisible ? "opacity-100" : "opacity-0 pointer-events-none"
      }`}
      aria-label="Scroll to top"
    >
      <ArrowUp className="w-5 h-5" />
    </button>
  );
};

export default Footer;
