"use client";
import Image from "next/image";
import Footer from "../../components/Footer";
import Head from "next/head";

export default function HowToUse() {
  return (
    <>
      <Head>
        <title>Keysentinel How To Use</title>
        <meta property="og:title" content="My page title" key="title" />
      </Head>
      <div className="min-h-screen bg-[#f4f4f4] text-[#161616] font-['IBM_Plex_Sans']">
        <div className="container mx-auto px-6 py-16 max-w-4xl">
          <h1 className="text-4xl font-semibold mb-10">
            How to Use Security Analysis
          </h1>

          <div className="grid md:grid-cols-2 gap-12 mb-14">
            <div>
              <ol className="space-y-8">
                {[
                  'Navigate to the "Security Analysis" page.',
                  "Provide your code file ",
                  "Select the programming language",
                  "Choose a predefined document or select 'Custom' to upload your own.",
                  "Provide a brief description of any security concerns you have (optional).",
                  'Click on "Analyze Code" to start the analysis.',
                  "The AI will review the document and provide security insights.",
                ].map((step, index) => (
                  <li key={index} className="flex gap-5">
                    <span className="flex-shrink-0 h-9 w-9 rounded-full bg-[#0f62fe]/10 text-[#0f62fe] flex items-center justify-center font-semibold text-lg">
                      {index + 1}
                    </span>
                    <span className="text-lg leading-relaxed">{step}</span>
                  </li>
                ))}
              </ol>
            </div>

            <div className="flex items-center justify-center">
              <Image
                src="/infoSign.jpg"
                alt="Security Analysis Example"
                width={350}
                height={250}
                className="rounded-lg border border-[#e0e0e0] shadow-md"
              />
            </div>
          </div>
        </div>

        <Footer />
      </div>
    </>
  );
}
