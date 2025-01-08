// Initial inventory (empty object to hold the items)
let inventory = {};

// Function to add an initial item to the inventory
function addInitialItem() {
    const itemName = document.getElementById('initialItem').value;
    const initialCount = parseInt(document.getElementById('initialCount').value);
    const imageInput = document.getElementById('initialImage');
    const imageFile = imageInput.files[0];

    if (itemName && initialCount > 0 && imageFile) {
        const reader = new FileReader();

        reader.onload = function(event) {
            const imageData = event.target.result; // Get the base64 image data

            // Store item details in the inventory object
            inventory[itemName] = {
                count: initialCount,
                image: imageData, // Base64 image data
                transactions: [] // To track transactions
            };

            updateItemList(); // Update the table to show the item
            alert("Item added successfully!");

            // Clear the form inputs after adding the item
            document.getElementById('initialItem').value = '';
            document.getElementById('initialCount').value = '';
            imageInput.value = '';
        };

        reader.readAsDataURL(imageFile); // Read the image as base64
    } else {
        alert("Please enter a valid item name, count, and upload an image.");
    }
}

// Function to take an item from the inventory
function takeItem() {
    const userName = document.getElementById('userName').value;
    const itemName = document.getElementById('itemTaken').value;
    const quantity = parseInt(document.getElementById('quantityTaken').value);
    const date = document.getElementById('dateTaken').value;

    if (inventory[itemName] && quantity > 0 && quantity <= inventory[itemName].count) {
        inventory[itemName].count -= quantity; // Decrease the item count
        inventory[itemName].transactions.push({
            user: userName,
            action: "take",
            quantity: quantity,
            date: date
        });

        updateItemList(); // Update the inventory list display
        alert("Item successfully taken!");
    } else {
        alert("Invalid quantity or item not available.");
    }
}

// Function to return an item to the inventory
function returnItem() {
    const userName = document.getElementById('userReturn').value;
    const itemName = document.getElementById('itemReturned').value;
    const quantity = parseInt(document.getElementById('quantityReturned').value);
    const date = document.getElementById('dateReturned').value;

    if (inventory[itemName] && quantity > 0) {
        inventory[itemName].count += quantity; // Increase the item count
        inventory[itemName].transactions.push({
            user: userName,
            action: "return",
            quantity: quantity,
            date: date
        });

        updateItemList(); // Update the inventory list display
        alert("Item successfully returned!");
    } else {
        alert("Invalid quantity or item does not exist.");
    }
}

// Function to update the inventory list display in the table
function updateItemList() {
    const inventoryTableBody = document.getElementById('inventoryTableBody');
    inventoryTableBody.innerHTML = '';  // Clear existing table rows

    for (const item in inventory) {
        const itemData = inventory[item];

        // Create a new table row for each item
        const row = document.createElement('tr');

        // Add the image, name, and count for each item
        row.innerHTML = `
            <td><img src="${itemData.image}" alt="${item}" class="inventory-image"></td>
            <td>${item}</td>
            <td>${itemData.count}</td>
        `;

        // Append the row to the table body
        inventoryTableBody.appendChild(row);
    }
}

// When the document is ready, run this to initialize the list (if needed)
document.addEventListener('DOMContentLoaded', function() {
    updateItemList();  // Initialize the inventory list (if any)
});

// When the form is submitted, show the confirmation message
const form = document.querySelector('form');
const confirmationMessage = document.getElementById('confirmation');

form.addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the form from reloading the page

    // Show confirmation message after form submission
    confirmationMessage.style.display = 'block';

    // Optionally, hide the form after submission
    form.style.display = 'none';

    // You can also implement AJAX here for smoother form submission without page reload
});

