var currentPage = 0;
var pageSize = 7; // Number of rows per page
var rows;

function initializeFileTable() {
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
    var fileTable = document.getElementById("file-table");

    addFileFormContainer.style.display = "none";
    fileTable.style.display = "table";

    // Optionally, you can clear the form fields if needed
    var addFileForm = document.getElementById("add-file-form");
    addFileForm.reset();
}

function showAddFileForm() {
    var addFileFormContainer = document.getElementById("add-file-form-container");
    var fileTable = document.getElementById("file-table");

    fileTable.style.display = "none";
    addFileFormContainer.style.display = "block";
}
