// Attach event listeners to buttons
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('addItemBtn').addEventListener('click', addInitialItem);
    document.getElementById('takeItemBtn').addEventListener('click', takeItem);
    document.getElementById('returnItemBtn').addEventListener('click', returnItem);
});
