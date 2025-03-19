"use client";
import Image from "next/image";
import { useRouter } from "next/navigation";
import "../styles/Home.css";

export default function Home() {
  let router = useRouter();
  const routeChange = () => {
    let path = `/how-to-use`;
    router.push(path);
  };
  return (
    <div className="container">
      <div className="content">
        <div className="text-section">
          <h1>AI Code Review & Security</h1>
          <p>Enhancing code quality and security with AI-powered insights.</p>
          <button className="cta-button" onClick={routeChange}>
            Get Started →
          </button>
        </div>
        <div className="image-section">
          <img src="Chatbot.jpg" alt="Chatbot" />
        </div>
      </div>
    </div>
  );
}
