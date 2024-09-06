import React, { useState } from 'react';
import Modal from './common/Modal';

const UploadPopup = ({ onFileUpload,sourceStack }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [uploadType, setUploadType] = useState('');
  const [file, setFile] = useState(null);
  const [githubLink, setGithubLink] = useState('');

  const handleUpload = () => {
    const formData = new FormData();

    if (uploadType === 'zip') {
      formData.append('file', file);
      formData.append('sourceStack', sourceStack);
    } else if (uploadType === 'github') {
      formData.append('github_link', githubLink);
      formData.append('sourceStack', sourceStack);

    }

    onFileUpload(formData);
    setIsOpen(false);
  };

  return (
    <div>
      <button
        onClick={() => setIsOpen(true)}
        className="w-full bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600"
      >
        Upload Project
      </button>

      {isOpen && (
        <Modal onClose={() => setIsOpen(false)}>
          <h2 className="text-xl font-bold mb-4">Select Upload Method</h2>
          <div className="mb-4">
            <label className="block mb-2">
              <input 
                type="radio" 
                name="uploadType" 
                value="zip"
                onChange={(e) => setUploadType(e.target.value)}
                className="mr-2"
              />
              Upload Zip File
            </label>
            <label className="block mb-4">
              <input 
                type="radio" 
                name="uploadType" 
                value="github"
                onChange={(e) => setUploadType(e.target.value)}
                className="mr-2"
              />
              Provide GitHub Link
            </label>
            {uploadType === 'zip' && (
              <input 
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
                className="p-2 border border-gray-300 rounded-lg w-full"
              />
            )}
            {uploadType === 'github' && (
              <input 
                type="text"
                placeholder="Enter GitHub repository link"
                value={githubLink}
                onChange={(e) => setGithubLink(e.target.value)}
                className="p-2 border border-gray-300 rounded-lg w-full"
              />
            )}
          </div>
          <div className="flex justify-end">
            <button 
              onClick={() => setIsOpen(false)} 
              className="bg-gray-300 text-gray-700 p-2 rounded-lg mr-2"
            >
              Cancel
            </button>
            <button 
              onClick={handleUpload}
              className="bg-blue-500 text-white p-2 rounded-lg"
            >
              Upload
            </button>
          </div>
        </Modal>
      )}
    </div>
  );
}

export default UploadPopup;
