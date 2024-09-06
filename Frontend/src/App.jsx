import React, { useState } from 'react';
import UploadPopup from './components/UploadPopup';
import ProjectStructure from './components/ProjectStructure';
import StackSelector from './components/StackSelector';
import ConvertButton from './components/ConvertButton';
import { uploadProject, convertProject } from './api';

const App = () => {
  const [sourceStack, setSourceStack] = useState('');
  const [targetStack, setTargetStack] = useState('');
  const [folderStructure, setFolderStructure] = useState(null);
  const [status, setStatus] = useState('');

  const handleFileUpload = async (data) => {
    setStatus('Uploading...');
    try {
      const result = await uploadProject(data);
      setFolderStructure(result.folderStructure);
      setStatus('Upload successful!');
    } catch (error) {
      setStatus('Upload failed. Please try again.');
    }
  };

  const handleConversion = async () => {
    setStatus('Converting...');
    try {
      await convertProject(sourceStack, targetStack, folderStructure);
      setStatus('Conversion successful!');
    } catch (error) {
      setStatus('Conversion failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-3xl bg-white p-6 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold text-center mb-8">Project Converter</h1>
        <StackSelector
          sourceStack={sourceStack}
          targetStack={targetStack}
          onSourceChange={(e) => setSourceStack(e.target.value)}
          onTargetChange={(e) => setTargetStack(e.target.value)}
        />
        <UploadPopup onFileUpload={handleFileUpload} sourceStack={sourceStack}/>
        {status && <p className="mt-4 text-center text-gray-600">{status}</p>}
        {folderStructure && (
          <div className="mt-6">
            <ProjectStructure structure={folderStructure} />
            <ConvertButton onConvert={handleConversion} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
