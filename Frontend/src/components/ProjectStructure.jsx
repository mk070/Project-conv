import React from 'react';
import TreeView from './TreeView';

const ProjectStructure = ({ structure }) => (
  <div className="bg-white p-4 rounded-lg shadow-lg">
    <h2 className="text-xl font-bold mb-4">Project Folder Structure</h2>
    <TreeView structure={structure} />
  </div>
);

export default ProjectStructure;
