document.addEventListener('DOMContentLoaded', function() {
  // Get the files link and main section element
  const filesLink = document.querySelector('#files-link');
  const mainSection = document.querySelector('#main-section');

  // Add click event listener to the files link
  filesLink.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default link behavior

    // Make an AJAX request to retrieve the file information
    const xhr = new XMLHttpRequest();
    xhr.open('GET', '/files', true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        // Update the content of the main section with the file information
        mainSection.innerHTML = xhr.responseText;
      }
    };
    xhr.send();
  });
});
