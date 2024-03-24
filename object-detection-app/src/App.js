import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [detectedObjects, setDetectedObjects] = useState([]);
  const [classCounts, setClassCounts] = useState({});
  const [uploading, setUploading] = useState(false);
  const [processedImage, setProcessedImage] = useState(null);
  const [imageName, setImageName] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);
  const [showUploadSection, setShowUploadSection] = useState(true);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setImageName(event.target.files[0].name);
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreviewImage(e.target.result);
    };
    reader.readAsDataURL(event.target.files[0]);
  };

  const handleUpload = () => {
    if (!selectedFile) {
      alert('Please select an image to upload.');
      return;
    }
    setUploading(true);
    const formData = new FormData();
    formData.append('image', selectedFile);

    axios.post('http://127.0.0.1:8000/api/detectobjects/', formData)
      .then(response => {
        setDetectedObjects(response.data.objects);
        setClassCounts(response.data.class_counts); // Update class counts state
        setProcessedImage(response.data.processed_image);
        setShowUploadSection(false); // Hide upload section after successful upload
        setUploading(false);
      })
      .catch(error => {
        console.error('Error uploading image:', error);
        setUploading(false);
      });
  };

  return (
    <div className="app-container">
      <div className="container">
        <nav className="navbar">
          <h1 className="brand">Object Detection Web App</h1>
        </nav>
        <div className="content">
          {showUploadSection ? (
            <div className="upload-section">
              <div className="image-box">
                <input type="file" id="imageInput" onChange={handleFileChange} accept="image/*" />
                <label htmlFor="imageInput" className="select-button">{imageName ? imageName : 'Select Image'}</label>
              </div>
              <button onClick={handleUpload} disabled={uploading} className="upload-button">
                {uploading ? 'Uploading...' : 'Upload Image'}
              </button>
            </div>
          ) : (
            <div className="image-section">
              <div className="original-image-container">
                <h2 className="section-title">Original Image:</h2>
                <img src={previewImage} alt="Original" className="original-image" />
              </div>
              <div className="processed-image-container">
                <h2 className="section-title">Processed Image:</h2>
                <img src={`data:image/jpeg;base64,${processedImage}`} alt="Processed" className="processed-image" />
              </div>
              <div className="dotted-line"></div>
            </div>
          )}
          {showUploadSection ? null : (
            <div className="results-section">
              <div className="centered-section">
                <h2 className="section-title">Total Objects Detected: {detectedObjects.length}</h2>
                <h2 className="section-title">Class Counts:</h2>
                <ul>
                  {Object.entries(classCounts).map(([className, count]) => (
                    <li key={className}>{className}: {count}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
