import React from 'react';

const StackSelector = ({ sourceStack, targetStack, onSourceChange, onTargetChange }) => (
  <div className="flex justify-between mb-6">
    <select 
      className="p-2 border border-gray-300 rounded-lg w-full mr-2"
      value={sourceStack} 
      onChange={onSourceChange}
    >
      <option value="" disabled>Select Source Stack</option>
      <option value="mern">MERN</option>
      <option value="springboot">Spring Boot</option>
      <option value="django">Django</option>
    </select>
    <select 
      className="p-2 border border-gray-300 rounded-lg w-full ml-2"
      value={targetStack} 
      onChange={onTargetChange}
    >
      <option value="" disabled>Select Target Stack</option>
      <option value="mern">MERN</option>
      <option value="springboot">Spring Boot</option>
      <option value="django">Django</option>
    </select>
  </div>
);

export default StackSelector;
