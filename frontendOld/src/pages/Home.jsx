import React from "react";
import "../styles/Home.css";
import { useNavigate } from "react-router-dom";

const Home = () => {
  let navigate = useNavigate(); 
  const routeChange = () =>{ 
    let path = `/how_to_use`; 
    navigate(path);
  }
  return (
    <div className="container">
      <div className="content">
      <div className="text-section">
        <h1>AI Code Review & Security</h1>
        <p>Enhancing code quality and security with AI-powered insights.</p>
        <button className="cta-button" onClick={routeChange}>Get Started →</button>
        </div>
        <div className="image-section">
          <img src="Chatbot.webp" alt="Chatbot" />
        </div>
      </div>
    </div>
  );
};

export default Home;
