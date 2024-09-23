document.addEventListener('DOMContentLoaded', function () {
    // Get the CSRF token from the page (Django includes this in the form)
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Function to send an AJAX request
    function sendAjaxRequest(url, data) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // Send CSRF token in the request header
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    // Add event listeners for status (checkbox) and role (select dropdown)
    document.querySelectorAll('input[type="checkbox"]').forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            const userId = this.id.split('-')[1];  // Get user id from the element's id
            var valueCheck = this.checked ? 1 : 0;

            console.log(`Status changed for user ${userId} to value ${valueCheck}!`);
            
            // Prepare the data
            const data = {
                user_id: userId,
                status: valueCheck
            };

            // Send an AJAX request to the server to update the status
            sendAjaxRequest('', data);  // Replace with your endpoint URL
        });
    });

    document.querySelectorAll('select').forEach(function (select) {
        select.addEventListener('change', function () {
            const userId = this.id.split('-')[1];  // Get user id from the element's id
            const valueSelected = this.value;

            console.log(`Role changed for user ${userId} to value ${valueSelected}!`);

            // Prepare the data
            const data = {
                user_id: userId,
                role: valueSelected
            };

            // Send an AJAX request to the server to update the role
            sendAjaxRequest('', data);  // Replace with your endpoint URL
        });
    });
});
