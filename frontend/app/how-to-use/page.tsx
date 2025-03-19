"use client";
import React from "react";
import "../../styles/HowToUse.css";
import Image from "next/image";

export default function How_To_Use() {
  return (
    <div className="container">
      <div className="content">
        <div className="text-section">
          <h1>How to use AI Code Review & Security:</h1>
          <p>1. Navigate to the to the "Code Review" page</p>
          <p>
            2. Click the on the "browse..." button and select a file to upload
            from your file explorer
          </p>
          <p>
            3. (Optional) Enter a brief description of the error your having
          </p>
          <p>
            4. State the programming language that used by the code in the file
            you uploaded
          </p>
          <p>
            5. Finally click on "Upload" and the AI will respond to your request
          </p>
        </div>
        <div className="flex justify-center">
          <Image 
            src="/infoSign.jpg" 
            alt="Example"
            width={300} 
            height={200}
            className="rounded-lg shadow-lg"
          />
        </div>
      </div>
    </div>
  );
}
