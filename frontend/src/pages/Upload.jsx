import React, { useState } from "react";
import "../styles/Upload.css";

const Upload = () => {
    const [file, setFile] = useState(null);

    const fileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const fileSubmit = (event) => {
        event.preventDefault();
        if(file) {
            console.log("File to be uploaded:", file);
        }
        else {
            console.log("No file detected.");
        }
    };

    return (
        <div className="upload-box">
            <h1>Upload Your File</h1>
            <form onSubmit={fileSubmit}>
                <input
                type = "file"
                onChange={fileChange}/>

                    <button type = "submit" className="upload-button">Upload</button>
            </form>

            {file && (
                <div className="file-info">
                    <p>File Name: {file.name}</p>
                    <p>File Size: {file.size}</p>
                    </div>
            )}

        </div>

);
};

export default Upload;