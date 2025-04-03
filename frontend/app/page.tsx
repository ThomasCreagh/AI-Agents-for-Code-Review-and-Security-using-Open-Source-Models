"use client";

import { useRouter } from "next/navigation";
import "../styles/Home.css";
// import { useEffect, useRef } from "react";
import Footer from "../components/Footer";
import ParticleCanvas from "../components/ParticleCanvas";

export default function Home() {
  const router = useRouter();
  // const canvasRef = useRef<HTMLCanvasElement>(null);
  //
  // useEffect(() => {
  //   const canvas = canvasRef.current;
  //   if (canvas) {
  //     const ctx = canvas.getContext("2d");
  //     if (ctx) {
  //       const setCanvasDimensions = () => {
  //         canvas.width = canvas.offsetWidth;
  //         canvas.height = canvas.offsetHeight;
  //       };
  //
  //       setCanvasDimensions();
  //       window.addEventListener("resize", setCanvasDimensions);
  //
  //       const particles: Particle[] = [];
  //       const particleCount = 50;
  //
  //       class Particle {
  //         x: number;
  //         y: number;
  //         size: number;
  //         speedX: number;
  //         speedY: number;
  //         color: string;
  //
  //         constructor() {
  //           if (canvas) {
  //             this.x = Math.random() * canvas.width;
  //             this.y = Math.random() * canvas.height;
  //             this.size = Math.random() * 3 + 1;
  //             this.speedX = (Math.random() - 0.5) * 0.5;
  //             this.speedY = (Math.random() - 0.5) * 0.5;
  //             this.color = "#0f62fe";
  //           }
  //         }
  //
  //         update() {
  //           this.x += this.speedX;
  //           this.y += this.speedY;
  //
  //           if (this.x > canvas.width) this.x = 0;
  //           else if (this.x < 0) this.x = canvas.width;
  //           if (this.y > canvas.height) this.y = 0;
  //           else if (this.y < 0) this.y = canvas.height;
  //         }
  //
  //         draw() {
  //           ctx.fillStyle = this.color;
  //           ctx.beginPath();
  //           ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
  //           ctx.fill();
  //         }
  //       }
  //
  //       for (let i = 0; i < particleCount; i++) {
  //         particles.push(new Particle());
  //       }
  //
  //       function animate() {
  //         if (canvas && ctx) {
  //           ctx.clearRect(0, 0, canvas.width, canvas.height);
  //
  //           for (let i = 0; i < particles.length; i++) {
  //             particles[i].update();
  //             particles[i].draw();
  //           }
  //
  //           requestAnimationFrame(animate);
  //         }
  //       }
  //
  //       animate();
  //
  //       return () => {
  //         window.removeEventListener("resize", setCanvasDimensions);
  //       };
  //     }
  //   }
  // }, []);
  //
  const handleGetStarted = () => {
    router.push(`/how-to-use`);
  };

  const aboutUs = () => {
    router.push(`/about`);
  };

  return (
    <>
      <div className="min-h-screen bg-white">
        <div className="relative overflow-hidden">
          <div className="absolute top-0 right-0 w-full h-full bg-[#f4f4f4] skew-y-6 transform origin-top-right -translate-y-1/2 -z-10 animate-pulse-slow"></div>
          <div className="absolute top-20 left-10 w-64 h-64 rounded-full bg-[#edf5ff] opacity-20 blur-3xl -z-10 animate-float"></div>
          <div className="absolute bottom-20 right-10 w-80 h-80 rounded-full bg-[#0f62fe] opacity-10 blur-3xl -z-10 animate-float-reverse"></div>

          <ParticleCanvas />

          <div className="container mx-auto px-4 py-16 md:py-24 mt-20">
            <div className="max-w-5xl mx-auto">
              <div className="text-center mb-16 animate-fade-in">
                <h1 className="-mt-6 text-6xl md:text-7xl lg:text-8xl font-semibold tracking-tight text-[#161616] leading-tight mb-10">
                  AI Code Review{" "}
                  <span className="text-[#0f62fe] relative inline-block">
                    &
                    <span className="absolute -bottom-2 left-0 w-full h-1 bg-[#0f62fe]"></span>
                  </span>{" "}
                  Security
                </h1>
                <p className="text-2xl md:text-3xl text-[#393939] max-w-2xl mx-auto mb-12">
                  Enhancing code quality and security with AI-powered insights.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
                  <button
                    onClick={handleGetStarted}
                    className="bg-[#0f62fe] hover:bg-[#0353e9] text-white font-medium px-10 py-5 transition-all flex items-center justify-center group text-lg"
                  >
                    Get Started
                    <span className="ml-2 group-hover:translate-x-1 transition-transform">
                      →
                    </span>
                  </button>
                </div>
              </div>

              <div className="animate-fade-in-delayed">
                <p className="text-base md:text-lg text-[#393939] mb-3 font-medium flex items-center justify-center">
                  <span className="w-5 h-0.5 bg-[#0f62fe] mr-2"></span>
                  CONNECT WITH US
                </p>
                <div className="flex flex-wrap gap-4 justify-center">
                  <a
                    href="https://www.instagram.com"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center bg-white border border-[#e0e0e0] hover:border-[#0f62fe] px-5 py-3 transition-colors group hover:shadow-md"
                  >
                    <div className="w-8 h-8 flex items-center justify-center text-[#0f62fe] mr-2 group-hover:scale-110 transition-transform">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <rect
                          x="2"
                          y="2"
                          width="20"
                          height="20"
                          rx="5"
                          ry="5"
                        ></rect>
                        <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                        <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
                      </svg>
                    </div>
                    <span className="text-lg text-[#161616] group-hover:text-[#0f62fe] transition-colors">
                      Instagram
                    </span>
                  </a>

                  <a
                    href="https://gitlab.com"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center bg-white border border-[#e0e0e0] hover:border-[#0f62fe] px-5 py-3 transition-colors group hover:shadow-md"
                  >
                    <div className="w-8 h-8 flex items-center justify-center text-[#0f62fe] mr-2 group-hover:scale-110 transition-transform">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M22.65 14.39L12 22.13 1.35 14.39a.84.84 0 0 1-.3-.94l1.22-3.78 2.44-7.51A.42.42 0 0 1 4.82 2a.43.43 0 0 1 .58 0 .42.42 0 0 1 .11.18l2.44 7.49h8.1l2.44-7.51A.42.42 0 0 1 18.6 2a.43.43 0 0 1 .58 0 .42.42 0 0 1 .11.18l2.44 7.49L23 13.45a.84.84 0 0 1-.35.94z"></path>
                      </svg>
                    </div>
                    <span className="text-lg text-[#161616] group-hover:text-[#0f62fe] transition-colors">
                      GitLab
                    </span>
                  </a>

                  <a
                    href="https://www.linkedin.com"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center bg-white border border-[#e0e0e0] hover:border-[#0f62fe] px-5 py-3 transition-colors group hover:shadow-md"
                  >
                    <div className="w-8 h-8 flex items-center justify-center text-[#0f62fe] mr-2 group-hover:scale-110 transition-transform">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
                        <rect x="2" y="9" width="4" height="12"></rect>
                        <circle cx="4" cy="4" r="2"></circle>
                      </svg>
                    </div>
                    <span className="text-lg text-[#161616] group-hover:text-[#0f62fe] transition-colors">
                      LinkedIn
                    </span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-[#f4f4f4] py-16 relative overflow-hidden animate-fade-in-delayed">
          <div className="absolute inset-0 bg-dots opacity-10"></div>

          <div className="container mx-auto px-4 relative">
            <div className="max-w-3xl mx-auto text-center">
              <div className="inline-block mb-6">
                <div className="w-16 h-1 bg-[#0f62fe] mx-auto mb-2"></div>
                <div className="w-8 h-1 bg-[#0f62fe] mx-auto"></div>
              </div>
              <h2 className="text-3xl font-semibold text-[#161616] mb-4">
                About This Project
              </h2>
              <p className="text-[#393939] mb-6">
                This AI Code Review & Security project was developed as part of
                the TCD Software Engineering program. It aims to demonstrate how
                artificial intelligence can be leveraged to improve code quality
                and security.
              </p>
              <button
                onClick={aboutUs}
                className="mt-4 inline-flex items-center text-[#0f62fe] font-medium hover:underline group"
              >
                Meet the team
                <span className="ml-2 group-hover:translate-x-1 transition-transform">
                  →
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
      <div className="container"> ... </div>
      <Footer />
    </>
  );
}
