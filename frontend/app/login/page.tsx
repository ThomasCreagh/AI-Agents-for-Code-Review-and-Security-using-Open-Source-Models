"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"

export default function Login() {
  const router = useRouter()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext("2d")
    if (!ctx) return

    const setCanvasDimensions = () => {
      canvas.width = canvas.offsetWidth
      canvas.height = canvas.offsetHeight
    }

    setCanvasDimensions()
    window.addEventListener("resize", setCanvasDimensions)

    const particles: Particle[] = []
    const particleCount = 50

    class Particle {
      x: number
      y: number
      size: number
      speedX: number
      speedY: number
      color: string

      constructor() {
        this.x = Math.random() * canvas.width
        this.y = Math.random() * canvas.height
        this.size = Math.random() * 3 + 1
        this.speedX = (Math.random() - 0.5) * 0.5
        this.speedY = (Math.random() - 0.5) * 0.5
        this.color = "#0f62fe"
      }

      update() {
        this.x += this.speedX
        this.y += this.speedY

        if (this.x > canvas.width) this.x = 0
        else if (this.x < 0) this.x = canvas.width
        if (this.y > canvas.height) this.y = 0
        else if (this.y < 0) this.y = canvas.height
      }

      draw() {
        ctx.fillStyle = this.color
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
        ctx.fill()
      }
    }

    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle())
    }

    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      for (let i = 0; i < particles.length; i++) {
        particles[i].update()
        particles[i].draw()
      }

      requestAnimationFrame(animate)
    }

    animate()

    return () => {
      window.removeEventListener("resize", setCanvasDimensions)
    }
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setIsLoading(true)

    try {
      // Here you would implement your actual authentication logic
      // This is a placeholder for demonstration
      await new Promise((resolve) => setTimeout(resolve, 1000))

      // Simulate successful login
      router.push("/dashboard")
    } catch (err) {
      setError("Invalid email or password")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-white flex flex-col justify-center">
      <div className="relative overflow-hidden">
        <div className="absolute top-0 right-0 w-full h-full bg-[#f4f4f4] skew-y-6 transform origin-top-right -translate-y-1/2 -z-10 animate-pulse-slow"></div>
        <div className="absolute top-20 left-10 w-64 h-64 rounded-full bg-[#edf5ff] opacity-20 blur-3xl -z-10 animate-float"></div>
        <div className="absolute bottom-20 right-10 w-80 h-80 rounded-full bg-[#0f62fe] opacity-10 blur-3xl -z-10 animate-float-reverse"></div>

        <canvas ref={canvasRef} className="absolute inset-0 w-full h-full -z-5 opacity-70 pointer-events-none"></canvas>

        <div className="container mx-auto px-4 py-16 relative z-10">
          <div className="max-w-md mx-auto bg-white p-8 border border-[#e0e0e0] shadow-lg animate-fade-in">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-semibold text-[#161616] mb-2">Welcome Back</h1>
              <p className="text-[#393939]">Sign in to your account</p>
            </div>

            {error && (
              <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
                <p className="text-red-700">{error}</p>
              </div>
            )}

            <form onSubmit={handleSubmit}>
              <div className="mb-6">
                <label htmlFor="email" className="block text-sm font-medium text-[#393939] mb-2">
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3 border border-[#e0e0e0] focus:border-[#0f62fe] focus:outline-none transition-colors"
                  placeholder="Enter your email"
                  required
                />
              </div>

              <div className="mb-6">
                <label htmlFor="password" className="block text-sm font-medium text-[#393939] mb-2">
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 border border-[#e0e0e0] focus:border-[#0f62fe] focus:outline-none transition-colors"
                  placeholder="Enter your password"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-[#0f62fe] hover:bg-[#0353e9] text-white font-medium px-6 py-4 transition-all flex items-center justify-center group text-lg disabled:opacity-70 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <span className="flex items-center">
                    <svg
                      className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      ></circle>
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      ></path>
                    </svg>
                    Signing in...
                  </span>
                ) : (
                  <span className="flex items-center">
                    Sign In
                    <span className="ml-2 group-hover:translate-x-1 transition-transform">→</span>
                  </span>
                )}
              </button>
            </form>

            <div className="mt-8 text-center">
              <p className="text-[#393939]">
                Don't have an account?{" "}
                <Link href="/signup" className="text-[#0f62fe] hover:underline font-medium">
                  Sign up
                </Link>
              </p>
            </div>
          </div>

          <div className="mt-8 text-center animate-fade-in-delayed">
            <Link href="/" className="inline-flex items-center text-[#0f62fe] font-medium hover:underline group">
              <span className="mr-2 group-hover:-translate-x-1 transition-transform">←</span>
              Back to home
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

