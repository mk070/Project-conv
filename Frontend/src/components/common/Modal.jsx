import React from 'react';

const Modal = ({ children, onClose }) => (
  <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
    <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-lg relative">
      {children}
      <button
        onClick={onClose}
        className="absolute top-2 right-2 bg-red-500 text-white p-1 rounded-full hover:bg-red-600"
      >
        &times;
      </button>
    </div>
  </div>
);

export default Modal;
