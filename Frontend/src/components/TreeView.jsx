import React from 'react';
import { AiFillFolder, AiFillFolderOpen, AiOutlineFile } from 'react-icons/ai';
import { MdArrowDropDown, MdArrowRight } from 'react-icons/md';

const TreeNode = ({ node }) => {
  const [expanded, setExpanded] = React.useState(false);

  const hasChildren = node.children && node.children.length > 0;

  const toggleExpand = () => {
    setExpanded(!expanded);
  };

  return (
    <div className="ml-4">
      <div
        onClick={toggleExpand}
        style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', position: 'relative' }}
      >
        <span style={{ position: 'absolute', left: '-16px', top: '6px' }}>
          {hasChildren && (expanded ? <MdArrowDropDown /> : <MdArrowRight />)}
        </span>
        <span style={{ marginRight: '8px' }}>
          {hasChildren ? (expanded ? <AiFillFolderOpen /> : <AiFillFolder />) : <AiOutlineFile />}
        </span>
        <strong>{node.name}</strong>
      </div>
      {expanded && hasChildren && (
        <div style={{ marginLeft: '16px', borderLeft: '1px solid #ccc', paddingLeft: '8px' }}>
          {node.children.map((child, index) => (
            <TreeNode key={index} node={child} />
          ))}
        </div>
      )}
    </div>
  );
};

const TreeView = ({ structure }) => {
  return (
    <div>
      {structure.map((node, index) => (
        <TreeNode key={index} node={node} />
      ))}
    </div>
  );
};

export default TreeView;
