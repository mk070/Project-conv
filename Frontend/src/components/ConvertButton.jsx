import React from 'react';

const ConvertButton = ({ onConvert }) => (
  <button
    onClick={onConvert}
    className="w-full bg-green-500 text-white p-2 rounded-lg hover:bg-green-600 mt-4"
  >
    Convert Project
  </button>
);

export default ConvertButton;
