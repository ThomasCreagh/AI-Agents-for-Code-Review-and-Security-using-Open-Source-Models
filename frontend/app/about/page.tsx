"use client";
import React, { useState } from "react";
import "../../styles/About.css";

const teamMembers = [
  { name: "Lucia Brown", img: "LuciaHeadshot.jpg" },
  { name: "Travis Yusuf", img: "TravisHeadshot.jpg" },
  { name: "Cuan Shaffrey", img: "CuanHeadshot.jpg" },
  { name: "Mohamed Ali", img: "MohamedHeadshot.jpg" },
  { name: "Jake Casserly", img: "JakeHeadshot.jpeg" },
  { name: "Thomas Keatinge Creagh", img: "TomHeadshot.jpeg" },
  { name: "Noah Scolard", img: "NoahHeadshot.jpg" },
  { name: "Anna Xue", img: "AnnaHeadshot.jpg" },
];

export default function About() {
  const [showDropdown, setShowDropdown] = useState(false);
  const [showDescription, setShowDescription] = useState(9); // 0 = Lucia, 1 = Travis, 2 = Cuan, 3 = Mohamad, 4 = ... , 9 = Nothing

  return (
    <div className="container">
      <div className="content">
        <div className="text-section">
          <h1>About Us</h1>
          <p>
            We are a team of passionate 2nd and 3rd-year Computer Science
            students at Trinity College, collaborating with IBM to develop an
            AI-powered code review system.
          </p>
          <p>
            Our goal is to automate code quality assessments and security
            testing, making software development faster, safer, and more
            efficient. As a startup project, we are still in the early stages,
            actively refining our system to ensure it meets industry standards.
          </p>
          <p>
            If you're interested in learning more about us or our project, feel
            free to reach out!
          </p>

          {/* Contact Us Button */}
          <button
            className="cta-button"
            onClick={() => setShowDropdown(!showDropdown)}
          >
            Contact Us ↓
          </button>

          {/* Dropdown Email List */}
          {showDropdown && (
            <div className="dropdown">
              <ul>
                <li>
                  Our Email:{" "}
                  <a href="mailto:tcdsweng2025group23@gmail.com">
                    tcdsweng2025group23@gmail.com
                  </a>
                </li>
                <li>
                  Instagram:{" "}
                  <a
                    href="https://www.instagram.com/keysentinel"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    @keysentinel
                  </a>
                </li>
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
                <img
                  src={`/${member.img}`}
                  alt={member.name}
                  className="team-photo"
                  onClick={() =>
                    showDescription !== index
                      ? setShowDescription(index)
                      : setShowDescription(9)
                  }
                />
                <p className="team-name">{member.name}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Description Section */}
        {showDescription === 0 && (
          <div className="text-section">
            <h2>Lucia Brown: </h2>
            <p>
              Developed an AI system last year for code analysis, generation,
              completion and translation between languages with IBM.
              Successfully implemented agile framework in the project to enter
              the SwEng showcase. Main experience is in Backend development in
              Python.
            </p>
          </div>
        )}

        {showDescription === 1 && (
          <div className="text-section">
            <h2>Travis Yusuf: </h2>
            <p>
              Developed a Legal Document Analysis Tool last year using LLMS, NER
              and, Relation Extraction for IBM. Represented the Data via
              Knowledge Graphs. Entered the SwEng Showcase. Main experience is
              backend dev in Python and Frontend React.
            </p>
          </div>
        )}

        {showDescription === 2 && (
          <div className="text-section">
            <h2>Cuan Shaffery: </h2>
            <p>
              Last year he worked with a company called Bounce. He was a member
              of the backend team and they developed a chatbot that could take
              in personal preferences and details about an individual and give
              recommendations on travel based on those details.
            </p>
          </div>
        )}

        {showDescription === 3 && (
          <div className="text-section">
            <h2>Mohamed Ali: </h2>
            <p>
              Developed a streamlined mortgage application process by
              identifying and addressing key bottlenecks, improving overall
              efficiency with CreditLogic. Main experience is with frontend
              using React.
            </p>
          </div>
        )}

        {showDescription === 4 && (
          <div className="text-section">
            <h2>Jake Casserly: </h2>
            <p>
              Currently Jake is working with Formula Trinity as the Control team
              lead in the AI team. He has also previously worked on a project
              involving commercial flight data where he used multithreading to
              improve the efficiency of the code.
            </p>
          </div>
        )}

        {showDescription === 5 && (
          <div className="text-section">
            <h2>Thomas Keating Creagh: </h2>
            <p>
              Previously when he worked at DLT Capital he made a location based
              house price index application for the Irish housing market, using
              Goland, Next.JS, MongoDB and python for analysing 20+ million
              lines of data. This was then used my MyHome.ie.
            </p>
          </div>
        )}

        {showDescription === 6 && (
          <div className="text-section">
            <h2>Noah Scolard: </h2>
            <p>
              Last year he worked with a group of students to create an
              application exploring commercial flight data, within the
              Programming Project module at Trinity. He worked on both frontend
              and backend aspects, creating a interactive experience through
              Processing.
            </p>
          </div>
        )}

        {showDescription === 7 && (
          <div className="text-section">
            <h2>Anna Xue: </h2>
            <p>
              Last year, as part of the Programming Project module, she worked
              on a team developing an application that analyzed and filtered
              flight data. She mainly worked on the frontend development, using
              Processing to implement interactive visualizations.{" "}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
