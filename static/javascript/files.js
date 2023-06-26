var currentPage = 0;
var pageSize = 7; // Number of rows per page
var rows;

function initializeFileTable() {
  var table = document.getElementById("file-table");
  rows = table.getElementsByTagName("tbody")[0].rows;
  showPage(currentPage);
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

document.addEventListener("DOMContentLoaded", function () {
  initializeFileTable();

  // Add event listener for the "Add File" button
  var addFileButton = document.getElementById("add-file-button");
  addFileButton.addEventListener("click", function () {
    var addFileFormContainer = document.getElementById("add-file-form-container");
    addFileFormContainer.style.display = "flex";
    addFileButton.style.display = "none";
  });

  // Add event listener for the "Cancel" button in the add file form
  var cancelButton = document.getElementById("cancel-button");
  cancelButton.addEventListener("click", function () {
    var addFileFormContainer = document.getElementById("add-file-form-container");
    var addFileButton = document.getElementById("add-file-button");

    // Hide the form container and display the "Add File" button
    addFileFormContainer.style.display = "none";
    addFileButton.style.display = "block";
  });

  // Add event listener for the document click to hide the form
  document.addEventListener("click", function (event) {
    var addFileFormContainer = document.getElementById("add-file-form-container");
    var addFileForm = document.getElementById("add-file-form");

    // Check if the clicked element is outside the form container or the form itself
    if (!addFileFormContainer.contains(event.target) && event.target !== addFileForm) {
      // Check if the form is empty
      var formFields = addFileForm.querySelectorAll("input, select");
      var isFormEmpty = true;
      formFields.forEach(function (field) {
        if (field.value.trim() !== "") {
          isFormEmpty = false;
        }
      });

      // Hide the form container if it is empty
      if (isFormEmpty) {
        addFileForm.reset();
        addFileFormContainer.style.display = "none";
        addFileButton.style.display = "block";
      }
    }
  });

  // Add event listener for the "Submit" button in the add file form
  var addFileForm = document.getElementById("add-file-form");
  addFileForm.addEventListener("submit", function (event) {
    event.preventDefault();
    var form = $(this);

    $.ajax({
      url: "/add-file",
      type: "POST",
      data: form.serialize(),
      success: function (response) {
        alert(response);
        location.reload(); // Refresh the page after adding the file
      },
      error: function (xhr) {
        alert("Error adding file: " + xhr.responseText);
      },
    });

    // Reset the form after submission
    addFileForm.reset();
    var addFileFormContainer = document.getElementById("add-file-form-container");
    var addFileButton = document.getElementById("add-file-button");
    addFileFormContainer.style.display = "none";
    addFileButton.style.display = "block";
  });
});
