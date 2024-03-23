document.addEventListener("DOMContentLoaded", function() {
    const rowsPerPage = 5;
    let currentPage = 1;
    let filteredRows = [];

    // Sorting functionality
    document.querySelectorAll("th").forEach(function(header, index) {
        header.addEventListener("click", function() {
            const isAscending = header.classList.contains("asc");
            sortTableByColumn(index, !isAscending);
            header.classList.toggle("asc", !isAscending);
            header.classList.toggle("desc", isAscending);
            paginate(1); // Reset to page 1 after sorting
        });
    });

    function sortTableByColumn(columnIndex, ascending) {
        const compare = function(rowA, rowB) {
            let valA = rowA.querySelector(`td:nth-child(${columnIndex + 1})`).textContent.trim();
            let valB = rowB.querySelector(`td:nth-child(${columnIndex + 1})`).textContent.trim();

            // Convert to comparable formats for Date and Rating columns
            if (columnIndex === 3) { // Date/Time column
                valA = new Date(valA).getTime();
                valB = new Date(valB).getTime();
            } else if (columnIndex === 2) {
                valA = parseInt(valA[0]);
                valB = parseInt(valB[0]);
            }

            return (
                valA > valB
                ? 1
                : (
                    valA < valB
                    ? -1
                    : 0
                )
            );
        };

        filteredRows.sort(function(a, b) { return compare(a, b) * (ascending ? 1 : -1); });
        updateTableDisplay();
    }

    // Filtering functionality
    document.getElementById("filterRating").addEventListener("change", function(event) {
        const rating = parseInt(event.target.value, 10);
        filterByRating(rating);
        paginate(1); // Reset to page 1 after filtering
    });

    function filterByRating(rating) {
        const allRows = document.querySelectorAll("table tbody tr");
        filteredRows = Array.from(allRows).filter(function(row) {
            const rowRating = parseInt(row.querySelector("td:nth-child(3)").textContent[0], 10);
            return rating === 0 || rowRating === rating;
        });
        updateTableDisplay();
    }

    // Pagination functionality
    document.getElementById("nextPage").addEventListener("click", function() {
        paginate(currentPage + 1);
    });

    document.getElementById("prevPage").addEventListener("click", function() {
        paginate(currentPage - 1);
    });

    function paginate(page) {
        const totalRows = filteredRows.length;
        const totalPages = Math.ceil(totalRows / rowsPerPage);
        currentPage = Math.max(1, Math.min(page, totalPages));

        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        const pageRows = filteredRows.slice(start, end);

        document.querySelectorAll("table tbody tr").forEach(function(row) {
            row.style.display = "none";
        });

        pageRows.forEach(function(row) {
            row.style.display = "";
        });

        document.getElementById("pageIndicator").textContent = `Page ${currentPage} of ${totalPages}`;
        document.getElementById("prevPage").disabled = currentPage === 1;
        document.getElementById("nextPage").disabled = currentPage === totalPages;
    }

    function updateTableDisplay() {
        document.querySelectorAll("table tbody tr").forEach(function(row) {
            row.style.display = "none";
        });

        filteredRows.forEach(function(row) {
            row.style.display = "";
        });

        paginate(currentPage);
    }

    document.getElementById("filterRating").addEventListener("change", function() {
        applyFilters();
    });

    // New event listener for the date picker
    document.getElementById("filterDate").addEventListener("change", function() {
        applyFilters();
    });

    function applyFilters() {
        const rating = parseInt(document.getElementById("filterRating").value, 10);
        const selectedDate = document.getElementById("filterDate").value;
        filterReviews(rating, selectedDate);
        paginate(1); // Reset to page 1 after filtering
    }

    function filterReviews(rating, selectedDate) {
        const allRows = document.querySelectorAll("table tbody tr");
        filteredRows = Array.from(allRows).filter(function(row) {
        const rowRating = parseInt(row.querySelector("td:nth-child(3)").textContent[0], 10);
        const rowDate = row.querySelector("td:nth-child(4)").textContent.trim();
        const dateMatch = (
    selectedDate
    ? new Date(rowDate).toDateString() === new Date(selectedDate).toDateString()
    : true
);
        return (rating === 0 || rowRating === rating) && dateMatch;
    });
    updateTableDisplay();
}
    // Initial setup
    applyFilters(); // Show all ratings and dates initially
});

