import './App.css';
import './style.css';
import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [label, setLabel] = useState(null);

  const onDrop = (acceptedFiles) => {
    // Update the state with the selected file
    setSelectedFile(acceptedFiles[0]);
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: ['.jpeg', '.png', '.jpg', '.JPG', '.PNG', '.JPEG'],
    maxFiles: 1,
  });

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form submission

    const formData = new FormData();
    formData.append("file", selectedFile, selectedFile.name);

    const requestOptions = {
      method: 'POST',
      body: formData,
    };

    try {
      const response = await fetch("http://localhost:8021/predict", requestOptions);
      const data = await response.json();

      const predictedClass = data.class;
      const confidence = data.confidence;

      setResult(confidence);
      setLabel(predictedClass);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <form>
        <div {...getRootProps()} className='dropzone'>
          <input {...getInputProps()} />
          {selectedFile ? (
            <img src={URL.createObjectURL(selectedFile)} alt="Selected" />
          ) : (
            <p>Drag & drop an image here, or click to select one</p>
          )}
        </div>
        <button onClick={handleSubmit} disabled={!selectedFile} className='upload-button'>
          Upload
        </button>
      </form>
      {result !== null && label !== null && (
        <div className='result-container'>
          <p className='result-header'>Result</p>
          <p className='result-text'>Label: {label}</p>
          {/* <p className='result-text'>Confidence: {result}</p> */}
        </div>
      )}
    </div>
  );
}
export default App;
