function getDomElementById(id) {
    return document.getElementById(id);
}

// Validate for English characters and space
function isEnglishText(text) {
    const englishTextPattern = /^[A-Za-z\s]+$/;
    return englishTextPattern.test(text);
}

// Check if a date is in the future
function isDateInFuture(date) {
    const today = new Date();
    const selectedDate = new Date(date);

    const todayDateOnly = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    const selectedDateOnly = new Date(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate());

    return selectedDateOnly > todayDateOnly;
}

function isValidDateFormat(date) {
    const dateFormatPattern = /^\d{4}-\d{2}-\d{2}$/; // Format: YYYY-MM-DD
    return dateFormatPattern.test(date);
}

function isValidHourFormat(hour) {
    const hourFormatPattern = /^\d{2}:\d{2}$/; // Format: HH:MM
    return hourFormatPattern.test(hour);
}

document.getElementById("flightCreationForm").addEventListener("submit", function (event) {
    // Assume all validations pass initially
    let allValidationsPass = true;

    // Get references for input values
    const departureInput = getDomElementById("departure");
    const destinationInput = getDomElementById("destination");
    const dateOfFlightInput = getDomElementById("dateOfFlight");
    const hourOfDepartureInput = getDomElementById("hourOfDeparture");
    const costEconomyInput = getDomElementById("costEconomy");
    const costPremiumInput = getDomElementById("costPremium");
    const costBusinessInput = getDomElementById("costBusiness");
    const flightDurationInput = getDomElementById("flightDuration");

    // Get input values
    const departure = departureInput.value;
    const destination = destinationInput.value;
    const dateOfFlight = dateOfFlightInput.value;
    const hourOfDeparture = hourOfDepartureInput.value;
    const costEconomy = parseFloat(costEconomyInput.value);
    const costPremium = parseFloat(costPremiumInput.value);
    const costBusiness = parseFloat(costBusinessInput.value);
    const flightDuration = parseFloat(flightDurationInput.value);

    // Validation for departure and destination fields
    if (!isEnglishText(departure) || !isEnglishText(destination)) {
        alert("Please enter only English letters in the fields.");
        allValidationsPass = false;
    }

    // Validation for date and hour format
    if (!isValidDateFormat(dateOfFlight)) {
        alert("Please enter the date in the format YYYY-MM-DD.");
        allValidationsPass = false;
    } else if (!isValidHourFormat(hourOfDeparture)) {
        alert("Please enter the hour in the format HH:MM.");
        allValidationsPass = false;
    }

    // Validation for non-negative values
    if (costEconomy <= 0 || costPremium <= 0 || costBusiness <= 0 || flightDuration <= 0) {
        alert("Cost values and flight duration must be positive numbers.");
        allValidationsPass = false;
    }

    // Validation for a future date
    if (!isDateInFuture(dateOfFlight)) {
        alert("The date of the flight must be a future date.");
        allValidationsPass = false;
    }

    // If any validation fails, prevent form submission
    if (!allValidationsPass) {
        event.preventDefault();
    }
    // If all validations pass, the form will submit normally.
});
