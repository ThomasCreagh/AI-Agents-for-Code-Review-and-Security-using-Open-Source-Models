"use client";

import React, { useState } from "react";
// import { useRouter } from "next/navigation";
import Link from "next/link";
import ParticleCanvas from "../../components/ParticleCanvas";
import Head from "next/head";
import { supabase } from "../../src/services/supabaseClient.js";

export default function SignUp() {
  // const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [confirmationMessage, setConfirmationMessage] = useState("");
  const [passwordStrength, setPasswordStrength] = useState("");

  const checkPasswordStrength = (password: string) => {
    let strength = "Weak";
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    if (
      password.length > 8 &&
      hasUpper &&
      hasLower &&
      hasNumber &&
      hasSpecial
    ) {
      strength = "Strong";
    } else if (
      password.length >= 6 &&
      (hasUpper || hasLower) &&
      (hasNumber || hasSpecial)
    ) {
      strength = "Medium";
    }
    setPasswordStrength(strength);
    console.log(passwordStrength);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!name.trim()) {
      setError("Name is required.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setIsLoading(true);

    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: { full_name: name },
        },
      });

      console.log(data);

      if (error) {
        setError(error.message);
      } else {
        setConfirmationMessage(
          "Signup successful! Please check your email to confirm your account.",
        );
      }
    } catch {
      setError("Signup failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  if (confirmationMessage) {
    return (
      <div className="min-h-screen bg-white flex flex-col justify-center">
        <div className="container mx-auto px-4 py-16 relative z-10">
          <div className="max-w-md mx-auto bg-white p-8 border border-[#e0e0e0] shadow-lg animate-fade-in">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-semibold text-[#161616] mb-2">
                Confirm Your Email
              </h1>
              <p className="text-[#393939]">{confirmationMessage}</p>
            </div>
            <div className="mt-8 text-center animate-fade-in-delayed">
              <Link
                href="/"
                className="inline-flex items-center text-[#0f62fe] font-medium hover:underline group"
              >
                <span className="mr-2 group-hover:-translate-x-1 transition-transform">
                  ←
                </span>
                Back to home
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>Keysentinel Signup</title>
        <meta property="og:title" content="My page title" key="title" />
      </Head>
      <div className="min-h-screen bg-white flex flex-col justify-center">
        <div className="relative overflow-hidden">
          <div className="absolute top-0 right-0 w-full h-full bg-[#f4f4f4] skew-y-6 transform origin-top-right -translate-y-1/2 -z-10 animate-pulse-slow"></div>
          <div className="absolute top-20 left-10 w-64 h-64 rounded-full bg-[#edf5ff] opacity-20 blur-3xl -z-10 animate-float"></div>
          <div className="absolute bottom-20 right-10 w-80 h-80 rounded-full bg-[#0f62fe] opacity-10 blur-3xl -z-10 animate-float-reverse"></div>

          <ParticleCanvas />

          <div className="container mx-auto px-4 py-16 relative z-10">
            <div className="max-w-md mx-auto bg-white p-8 border border-[#e0e0e0] shadow-lg animate-fade-in">
              <div className="text-center mb-8">
                <h1 className="text-3xl font-semibold text-[#161616] mb-2">
                  Create Account
                </h1>
                <p className="text-[#393939]">Sign up to get started</p>
              </div>

              {error && (
                <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
                  <p className="text-red-700">{error}</p>
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="mb-6">
                  <label
                    htmlFor="name"
                    className="block text-sm font-medium text-[#393939] mb-2"
                  >
                    Name
                  </label>
                  <input
                    id="name"
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full px-4 py-3 border border-[#e0e0e0] focus:border-[#0f62fe] focus:outline-none transition-colors"
                    placeholder="Enter your name"
                    required
                  />
                </div>

                <div className="mb-6">
                  <label
                    htmlFor="email"
                    className="block text-sm font-medium text-[#393939] mb-2"
                  >
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
                  <label
                    htmlFor="password"
                    className="block text-sm font-medium text-[#393939] mb-2"
                  >
                    Password
                  </label>
                  <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full px-4 py-3 border border-[#e0e0e0] focus:border-[#0f62fe] focus:outline-none transition-colors"
                    placeholder="Create a password"
                    required
                  />
                </div>

                <div className="mb-6">
                  <label
                    htmlFor="confirmPassword"
                    className="block text-sm font-medium text-[#393939] mb-2"
                  >
                    Confirm Password
                  </label>
                  <input
                    id="confirmPassword"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full px-4 py-3 border border-[#e0e0e0] focus:border-[#0f62fe] focus:outline-none transition-colors"
                    placeholder="Confirm your password"
                    required
                  />
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-[#0f62fe] hover:bg-[#0353e9] text-white font-medium px-6 py-4 transition-all flex items-center justify-center group text-lg disabled:opacity-70 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <>
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
                      Creating account...
                    </>
                  ) : (
                    <span className="flex items-center">
                      Sign Up
                      <span className="ml-2 group-hover:translate-x-1 transition-transform">
                        →
                      </span>
                    </span>
                  )}
                </button>
              </form>

              <div className="mt-8 text-center">
                <p className="text-[#393939]">
                  Already have an account?{" "}
                  <Link
                    href="/login"
                    className="text-[#0f62fe] hover:underline font-medium"
                  >
                    Log in
                  </Link>
                </p>
              </div>
            </div>

            {error && (
              <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
                <p className="text-red-700">{error}</p>
              </div>
            )}

            <form onSubmit={handleSubmit}>
              <div className="mb-6">
                <label
                  htmlFor="name"
                  className="block text-sm font-medium text-[#393939] mb-2"
                >
                  Name
                </label>
                <input
                  id="name"
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-4 py-3 border border-[#e0e0e0] focus:border-[#0f62fe] focus:outline-none transition-colors"
                  placeholder="Enter your name"
                  required
                />
              </div>

              <div className="mb-6">
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-[#393939] mb-2"
                >
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
                <label
                  htmlFor="password"
                  className="block text-sm font-medium text-[#393939] mb-2"
                >
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    checkPasswordStrength(e.target.value);
                  }}
                  className="w-full px-4 py-3 border border-[#e0e0e0] focus:border-[#0f62fe] focus:outline-none transition-colors"
                  placeholder="Create a password"
                  required
                />
              </div>

              <div className="mb-6">
                <label
                  htmlFor="confirmPassword"
                  className="block text-sm font-medium text-[#393939] mb-2"
                >
                  Confirm Password
                </label>
                <input
                  id="confirmPassword"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full px-4 py-3 border border-[#e0e0e0] focus:border-[#0f62fe] focus:outline-none transition-colors"
                  placeholder="Confirm your password"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-[#0f62fe] hover:bg-[#0353e9] text-white font-medium px-6 py-4 transition-all flex items-center justify-center group text-lg disabled:opacity-70 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <>
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
                    Creating account...
                  </>
                ) : (
                  <span className="flex items-center">
                    Sign Up
                    <span className="ml-2 group-hover:translate-x-1 transition-transform">
                      →
                    </span>
                  </span>
                )}
              </button>
            </form>

            <div className="mt-8 text-center">
              <p className="text-[#393939]">
                Already have an account?{" "}
                <Link
                  href="/login"
                  className="text-[#0f62fe] hover:underline font-medium"
                >
                  Log in
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
