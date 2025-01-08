// Add event listener to handle form submission
document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Get form data
    const userName = document.querySelector('input[name="user_name"]').value;
    const itemId = document.querySelector('select[name="item_id"]').value;
    const quantity = document.querySelector('input[name="quantity"]').value;
    const date = document.querySelector('input[name="date"]').value;

    // Data to send via AJAX
    const data = {
        user_name: userName,
        item_id: itemId,
        quantity: quantity,
        date: date,
        csrfmiddlewaretoken: document.querySelector('[name="csrfmiddlewaretoken"]').value // CSRF token for security
    };

    // Send the data to the backend via AJAX (using fetch API)
    fetch('{% url "return_item" %}', {
        method: 'POST',
        body: new URLSearchParams(data), // Send the form data as URL parameters
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Display success popup
            alert('Item successfully returned!');

            // Redirect to index page (inventory page)
            window.location.href = '{% url "inventory" %}';
        } else {
            // Handle error (e.g., item not found, insufficient quantity)
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        // Handle any other errors
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
});
