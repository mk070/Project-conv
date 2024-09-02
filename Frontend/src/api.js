export const uploadProject = async (data) => {
    const response = await fetch('http://localhost:8000/api/upload/', {
      method: 'POST',
      body: data,
    });
  
    if (!response.ok) {
      throw new Error('Upload failed');
    }
  
    return response.json();
  };
  
export const convertProject = async (sourceStack, targetStack, folderStructure) => {
    const response = await fetch('http://localhost:8000/api/convert/', {
      method: 'POST',
      body: JSON.stringify({
        sourceStack,
        targetStack,
        folderStructure,
      }),
      headers: {
        'Content-Type': 'application/json',
      },
    });
  
    if (!response.ok) {
      throw new Error('Conversion failed');
    }
  
    return response.json();
  };
  