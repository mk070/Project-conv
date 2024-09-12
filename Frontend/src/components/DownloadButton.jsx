import React from 'react';

const DownloadButton = ({ onDownload }) => (
  <button
    onClick={onDownload}
    className="w-full bg-green-500 text-white p-2 rounded-lg hover:bg-green-600 mt-4"
  >
    Download Project
  </button>
);

export default DownloadButton;

