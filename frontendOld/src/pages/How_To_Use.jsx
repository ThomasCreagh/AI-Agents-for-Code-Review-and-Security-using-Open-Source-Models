import React from "react";
import "../styles/How_To_Use.css";

const How_To_Use = () => {
  return (
    <div className="container">
      <div className="content">
      <div className="text-section">
        <h1>How to use AI Code Review & Security:</h1>
        <p>1. Navigate to the to the "Code Review" page</p>
        <p>2. Click the on the "browse..." button and select a file to upload from your file explorer</p>
        <p>3. Enter a brief description of the error your having</p>
        <p>4. (Optional) Submit the relavent documentation for your uploaded code</p>
        <p>5. State the programming language that used by the code in the file you uploaded</p>
        <p>6. Finally click on "Upload" and the AI will respond to your request</p>
        </div>
        <div className="info-image">
          <img src="infoSign.webp" alt="info-sign"/>
        </div>
      </div>
    </div>
  );
};

export default How_To_Use;