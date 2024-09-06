def remove_code_markers(response):
    markers = ["```python", "```plaintext", "```"]

    # Check if the response starts and ends with any of the markers
    for marker in markers:
        if response.startswith(marker):
            response = response[len(marker):].lstrip()  # Remove the marker and leading whitespace
        if response.endswith(marker):
            response = response[:-len(marker)].rstrip()  # Remove the marker and trailing whitespace
    
    # Check if the response contains any of the markers
    if "```" in response:
        response = response.replace("```", '')

    # Check if the response contains any of the markers with language names
    marker_names = ["python", "plaintext"]
    for marker in marker_names:
        if f"```{marker}" in response:
            response = response.replace(f"```{marker}", '')

    return response