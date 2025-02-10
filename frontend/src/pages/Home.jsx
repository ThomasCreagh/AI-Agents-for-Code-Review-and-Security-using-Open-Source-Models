import React from "react";
import "../styles/Home.css";

const Home = () => {
  return (
    <div className="container">
      <div className="content">
      <div className="text-section">
        <h1>AI Code Review & Security</h1>
        <p>Enhancing code quality and security with AI-powered insights.</p>
        <button className="cta-button">Get Started →</button>
        </div>
        <div className="image-section">
          <img src="Chatbot.jpg" alt="Chatbot" />
        </div>
      </div>
    </div>
  );
};

export default Home;
