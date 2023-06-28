var currentPage = 0;
var pageSize = 7; // Number of rows per page
var rows;

function initializeFileTable() {
  // hhhhhhhhhhhhhhhhhhhhhhh
 var addFileForm = document.getElementById("add-file-form");
addFileForm.addEventListener("submit", handleSubmit);
  //hhhhhhhhhhhhhhhhhhhhhhhh
    try {
        var table = document.getElementById("file-table");
        if (table) {
            var tbody = table.getElementsByTagName("tbody")[0];
            if (tbody) {
                rows = tbody.rows;
                showPage(currentPage);
            }
        }

        var cancelButton = document.getElementById("cancel-button");
        cancelButton.addEventListener("click", hideAddFileForm);
    } catch (error) {
        console.error('An error occurred:', error);
    }
}

function showPage(page) {
    var startIndex = page * pageSize;
    var endIndex = startIndex + pageSize;

    for (var i = 0; i < rows.length; i++) {
        if (i >= startIndex && i < endIndex) {
            rows[i].style.display = "table-row";
        } else {
            rows[i].style.display = "none";
        }
    }
}

function previousPage() {
    if (currentPage > 0) {
        currentPage--;
        showPage(currentPage);
    }
}

function nextPage() {
    if (currentPage < rows.length / pageSize - 1) {
        currentPage++;
        showPage(currentPage);
    }
}

function searchFiles() {
    var input = document.getElementById("search-input").value.toUpperCase();

    for (var i = 0; i < rows.length; i++) {
        var fileNumber = rows[i].cells[0].innerText.toUpperCase();
        var dateAdded = rows[i].cells[1].innerText.toUpperCase();
        var category = rows[i].cells[2].innerText.toUpperCase();
        var refNum = rows[i].cells[3].innerText.toUpperCase();
        var title = rows[i].cells[4].innerText.toUpperCase();
        var status = rows[i].cells[5].innerText.toUpperCase();

        if (input === "") {
            showPage(currentPage); // Display the current page without filtering
            return;
        } else if (
            fileNumber.indexOf(input) > -1 ||
            dateAdded.indexOf(input) > -1 ||
            category.indexOf(input) > -1 ||
            refNum.indexOf(input) > -1 ||
            title.indexOf(input) > -1 ||
            status.indexOf(input) > -1
        ) {
            rows[i].style.display = "table-row";
        } else {
            rows[i].style.display = "none";
        }
    }
}



function hideAddFileForm() {
    var addFileFormContainer = document.getElementById("add-file-form-container");

    // Hide only the form, not the entire container
    var addFileForm = document.getElementById("add-file-form");
    addFileFormContainer.style.display = "none";

    // Optionally, you can clear the form fields if needed
    addFileForm.reset();

    // Show the "Add File" button
    var addFileButton = document.getElementById("add-file-button");
    addFileButton.style.display = "inline-block";
}




function showAddFileForm() {
    var addFileFormContainer = document.getElementById("add-file-form-container");

    addFileFormContainer.style.display = "block";
}


function handleSubmit(event) {
  event.preventDefault(); // Prevent the default form submission behavior
  
  // Retrieve the form input values
  var categoryInput = document.getElementsByName("category")[0].value;
  var refNumInput = document.getElementsByName("ref_num")[0].value;
  var titleInput = document.getElementsByName("title")[0].value;
  var statusInput = document.getElementsByName("status")[0].value;
  
  // Create an object with the form data
  var formData = {
    
    category: categoryInput,
    ref_num: refNumInput,
    title: titleInput,
    status: statusInput
  };
  
  // Send the form data to the server
  fetch('/file_table', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData)
  })
    .then(response => {
      if (response.ok) {
        // Redirect to another page after successful submission
        window.location.href = '/files';
      } else {
        throw new Error('Error: ' + response.status);
      }
    })
    .catch(error => {
      console.error('An error occurred:', error);
    });
  
  // Hide the form and show the "Add File" button
  hideAddFileForm();
}





