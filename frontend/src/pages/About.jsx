import React, { useState } from "react";
import "../styles/About.css";

const teamMembers = [
    { name: "Lucia Brown", img: "LuciaHeadShot.jpg" },
    { name: "Tavis Yusuf", img: "TravisHeadshot.jpg" },
    { name: "Cuan Shaffrey", img: "CuanHeadshot.jpg" },
    { name: "Mohamed Ali", img: "MohamedHeadshot.jpg" },
    { name: "Jake Casserly", img: "JakeHeadshot.jpeg" },
    { name: "Thomas Keatinge Creagh", img: "TomHeadshot.jpeg" },
    { name: "Noah Scolard", img: "NoahHeadshot.jpg" },
    { name: "Anna Xue", img: "AnnaHeadshot.jpg" }
];

const About = () => {
  const [showDropdown, setShowDropdown] = useState(false);

  return (
    <div className="container">
      <div className="content">
        <div className="text-section">
          <h1>About Us</h1>
          <p>
            We are a team of passionate 2nd and 3rd-year Computer Science students at Trinity College, 
            collaborating with IBM to develop an AI-powered code review system.
          </p>
          <p>
            Our goal is to automate code quality assessments and security testing, making software development 
            faster, safer, and more efficient. As a startup project,
             we are still in the early stages, actively refining our system to ensure it meets industry standards.
          </p>
          <p>
            If you're interested in learning more about us or our project, feel free to reach out!
          </p>

          {/* Contact Us Button */}
          <button className="cta-button" onClick={() => setShowDropdown(!showDropdown)}>
            Contact Us ↓
          </button>

          {/* Dropdown Email List */}
          {showDropdown && (
            <div className="dropdown">
              <ul>
                <li>Our Email: <a href="mailto:tcdsweng2025group23@gmail.com">tcdsweng2025group23@gmail.com</a></li>
                <li>Instagram: <a href="https://www.instagram.com/keysentinel" target="_blank" rel="noopener noreferrer">@keysentinel</a></li>
              </ul>
            </div>
          )}
        </div>

        {/* Team Members Section */}
        <div className="team-section">
          <h2>Meet Our Team</h2>
          <div className="team-grid">
            {teamMembers.map((member, index) => (
              <div key={index} className="team-member">
                <img src={`${process.env.PUBLIC_URL}/${member.img}`} alt={member.name} className="team-photo" />
                <p className="team-name">{member.name}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
