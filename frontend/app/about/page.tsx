"use client"
import { useState, useRef, useEffect } from "react"
import Footer from "../../components/Footer";

const teamMembers = [
  { name: "Lucia Brown", img: "LuciaHeadshot.jpg", role: "Backend Developer" },
  { name: "Travis Yusuf", img: "TravisHeadshot.jpg", role: "AI Developer" },
  { name: "Cuan Shaffrey", img: "CuanHeadshot.jpg", role: "Frontend Developer" },
  { name: "Mohamed Ali", img: "MohamedHeadshot.jpg", role: "Frontend Developer" },
  { name: "Jake Casserly", img: "JakeHeadshot.jpeg", role: "Frontend Developer" },
  { name: "Thomas Keatinge Creagh", img: "TomHeadshot.jpeg", role: "Backend Developer" },
  { name: "Noah Scolard", img: "NoahHeadshot.jpg", role: "AI Developer" },
  { name: "Anna Xue", img: "AnnaHeadshot.jpg", role: "Frontend Developer" },
]

const teamDescriptions = [
  "Developed an AI system last year for code analysis, generation, completion and translation between languages with IBM. Successfully implemented agile framework in the project to enter the SwEng showcase. Main experience is in Backend development in Python.",
  "Developed a Legal Document Analysis Tool last year using LLMS, NER and, Relation Extraction for IBM. Represented the Data via Knowledge Graphs. Entered the SwEng Showcase. Main experience is backend dev in Python and Frontend React.",
  "Last year he worked with a company called Bounce. He was a member of the backend team and they developed a chatbot that could take in personal preferences and details about an individual and give recommendations on travel based on those details.",
  "Developed a streamlined mortgage application process by identifying and addressing key bottlenecks, improving overall efficiency with CreditLogic. Main experience is with frontend using React.",
  "Currently Jake is working with Formula Trinity as the Control team lead in the AI team. He has also previously worked on a project involving commercial flight data where he used multithreading to improve the efficiency of the code.",
  "Previously when he worked at DLT Capital he made a location based house price index application for the Irish housing market, using Goland, Next.JS, MongoDB and python for analysing 20+ million lines of data. This was then used my MyHome.ie.",
  "Last year he worked with a group of students to create an application exploring commercial flight data, within the Programming Project module at Trinity. He worked on both frontend and backend aspects, creating a interactive experience through Processing.",
  "Last year, as part of the Programming Project module, she worked on a team developing an application that analyzed and filtered flight data. She mainly worked on the frontend development, using Processing to implement interactive visualizations.",
]

export default function About() {
  const [showDropdown, setShowDropdown] = useState(false)
  const [showDescription, setShowDescription] = useState(9) // 0 = Lucia, 1 = Travis, 2 = Cuan, 3 = Mohamad, 4 = ... , 9 = Nothing
  const [scrolled, setScrolled] = useState(false)
  const descriptionRef = useRef(null)

  // Scroll to description when it changes
  useEffect(() => {
    if (showDescription !== 9 && descriptionRef.current) {
      const element = descriptionRef.current
      const yOffset = -100 // Offset to account for any fixed headers
      const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset

      window.scrollTo({
        top: y,
        behavior: "smooth",
      })
    }
  }, [showDescription])

  return (
    <>
    <div className="min-h-screen bg-white py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* About Section */}
        <div className="mb-16 max-w-3xl mx-auto text-center">
          <h1 className="text-4xl font-bold text-[#161616] mb-6 relative inline-block">
            About Us
            <span className="absolute bottom-0 left-0 w-full h-1 bg-[#0f62fe] transform -translate-y-2"></span>
          </h1>
          <p className="text-lg text-[#393939] mb-6">
            We are a team of passionate 2nd and 3rd-year Computer Science students at Trinity College, collaborating
            with IBM to develop an AI-powered code review system.
          </p>
          <p className="text-lg text-[#393939] mb-6">
            Our goal is to automate code quality assessments and security testing, making software development faster,
            safer, and more efficient. As a startup project, we are still in the early stages, actively refining our
            system to ensure it meets industry standards.
          </p>
          <p className="text-lg text-[#393939] mb-8">
            If you're interested in learning more about us or our project, feel free to reach out!
          </p>
          
        {/* Connect With Us Section */}
        <div className="mt-12 animate-fade-in-delayed">
          <p className="text-base md:text-lg text-[#393939] mb-3 font-medium flex items-center justify-center">
            <span className="w-5 h-0.5 bg-[#0f62fe] mr-2"></span>
            CONNECT WITH US
          </p>
          <div className="flex flex-wrap gap-4 justify-center">
            {/* Email */}
            <a
              href="mailto:tcdsweng2025group23@gmail.com"
              className="flex items-center bg-white border border-[#e0e0e0] hover:border-[#0f62fe] px-5 py-3 transition-colors group hover:shadow-md"
            >
              <div className="w-8 h-8 flex items-center justify-center text-[#0f62fe] mr-2 group-hover:scale-110 transition-transform">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                  <path d="M3 8l9 6 9-6M4 6h16a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V8a2 2 0 012-2z" />
                </svg>
              </div>
              <span className="text-lg text-[#161616] group-hover:text-[#0f62fe] transition-colors">
                tcdsweng2025group23@gmail.com
              </span>
            </a>

            {/* Instagram */}
            <a
              href="https://www.instagram.com/keysentinel"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center bg-white border border-[#e0e0e0] hover:border-[#0f62fe] px-5 py-3 transition-colors group hover:shadow-md"
            >
              <div className="w-8 h-8 flex items-center justify-center text-[#0f62fe] mr-2 group-hover:scale-110 transition-transform">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                  <rect x="2" y="2" width="20" height="20" rx="5" ry="5" />
                  <path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37z" />
                  <line x1="17.5" y1="6.5" x2="17.51" y2="6.5" />
                </svg>
              </div>
              <span className="text-lg text-[#161616] group-hover:text-[#0f62fe] transition-colors">
                @keysentinel
              </span>
            </a>

            {/* LinkedIn */}
            <a
              href="https://www.linkedin.com/company/tcd-scss-sweng/"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center bg-white border border-[#e0e0e0] hover:border-[#0f62fe] px-5 py-3 transition-colors group hover:shadow-md"
            >
              <div className="w-8 h-8 flex items-center justify-center text-[#0f62fe] mr-2 group-hover:scale-110 transition-transform">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                  <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z" />
                  <rect x="2" y="9" width="4" height="12" />
                  <circle cx="4" cy="4" r="2" />
                </svg>
              </div>
              <span className="text-lg text-[#161616] group-hover:text-[#0f62fe] transition-colors">
                LinkedIn
              </span>
            </a>
          </div>
        </div>
      </div>

        {/* Team Members Section with Description */}
        <div className="mb-16 relative">
          <h2 className="text-3xl font-semibold text-[#161616] mb-10 text-center">Meet Our Team</h2>

          {/* Description Section - Now positioned above the team grid */}
          {showDescription !== 9 && (
            <div
              ref={descriptionRef}
              className="max-w-4xl mx-auto mb-12 bg-white p-8 rounded-lg shadow-xl border-l-4 border-[#0f62fe] animate-fade-in relative z-10"
            >
              <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
                <div className="w-24 h-24 md:w-32 md:h-32 rounded-full overflow-hidden border-4 border-[#0f62fe] shadow-lg flex-shrink-0 mx-auto md:mx-0">
                  <img
                    src={`/${teamMembers[showDescription].img}`}
                    alt={teamMembers[showDescription].name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="flex-1">
                  <div className="flex justify-between items-start">
                    <div>
                      <h2 className="text-2xl font-bold text-[#161616] mb-1">{teamMembers[showDescription].name}</h2>
                      <p className="text-[#0f62fe] font-medium mb-4">{teamMembers[showDescription].role}</p>
                    </div>
                    <button
                      onClick={() => setShowDescription(9)}
                      className="text-gray-500 hover:text-[#0f62fe] transition-colors"
                      aria-label="Close"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-6 w-6"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                  <p className="text-[#393939] leading-relaxed text-lg">{teamDescriptions[showDescription]}</p>
                </div>
              </div>

              {/* Decorative elements */}
              <div className="absolute -bottom-2 -right-2 w-20 h-20 bg-[#edf5ff] rounded-full opacity-50 z-0"></div>
              <div className="absolute -top-2 -left-2 w-12 h-12 bg-[#0f62fe] rounded-full opacity-10 z-0"></div>
            </div>
          )}

          {/* Team Grid */}
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
            {teamMembers.map((member, index) => (
              <div
                key={index}
                className={`text-center transition-all duration-300 transform ${showDescription === index ? "scale-105" : "hover:scale-105"}`}
              >
                <div
                  className={`relative overflow-hidden rounded-lg mb-4 cursor-pointer shadow-md transition-all duration-300 ${
                    showDescription === index
                      ? "ring-4 ring-[#0f62fe] shadow-lg shadow-[#0f62fe]/20"
                      : "hover:shadow-lg"
                  }`}
                  onClick={() => (showDescription !== index ? setShowDescription(index) : setShowDescription(9))}
                >
                  <img
                    src={`/${member.img}`}
                    alt={member.name}
                    className="w-full h-64 object-cover object-center transition-transform duration-500 hover:scale-110"
                  />
                  <div
                    className={`absolute inset-0 bg-gradient-to-t from-black/70 to-transparent transition-opacity duration-300 flex flex-col justify-end p-4 ${
                      showDescription === index ? "opacity-100" : "opacity-0 hover:opacity-100"
                    }`}
                  >
                    <p className="text-white font-medium">
                      {showDescription === index ? "Selected" : "Click for details"}
                    </p>
                  </div>
                </div>
                <h3 className="font-semibold text-lg text-[#161616]">{member.name}</h3>
                <p className="text-sm text-[#393939]">{member.role}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
        <div className="container"> ... </div>
    <Footer />
  </>
  )
}

