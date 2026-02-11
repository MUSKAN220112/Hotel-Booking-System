// JavaScript Helper Functions for Date Handling, API Calls, Alerts, and Hotel Search Functionality

// Function to handle date formatting
function formatDate(date) {
    return date.toISOString().slice(0, 19).replace('T', ' ');
}

// Function to make API calls
async function makeApiCall(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error making API call:', error);
    }
}

// Function to show alerts
function showAlert(message) {
    alert(message);
}

// Function to search for hotels
async function searchHotels(destination, checkInDate, checkOutDate) {
    const url = `https://api.example.com/hotels?destination=${destination}&checkIn=${formatDate(checkInDate)}&checkOut=${formatDate(checkOutDate)}`;
    const hotels = await makeApiCall(url);
    return hotels;
}