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
  

  export const downloadProject = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/download/', {
        method: 'GET',
      });
  
      if (response.ok) {
        // Convert response into a Blob
        const blob = await response.blob();
  
        // Create a URL for the blob object
        const url = window.URL.createObjectURL(blob);
        
        // Create a temporary <a> element to trigger the download
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'django_converted.zip');  // Set the file name
        
        // Append the link to the document body and trigger the download
        document.body.appendChild(link);
        link.click();
        
        // Clean up: remove the link after triggering the download
        link.parentNode.removeChild(link);
      } else {
        console.error('Failed to download zip file:', response.statusText);
      }
    } catch (error) {
      console.error('Error downloading the zip file:', error);
    }
  };