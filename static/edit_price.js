document.querySelectorAll('input[name="price"]').forEach(input => {
    input.addEventListener('blur', function() {
        const contentId = this.dataset.contentId;  // Get the option ID from the data attribute
        const newValue = this.value;  // Get the updated value

        // Fetch the CSRF token from the cookie
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        fetch('', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,  // Use the fetched CSRF token
            },
            body: JSON.stringify({
                'price': newValue,
                'content_id': contentId
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update price');
            }
            return response.json();
        })
        .then(data => {
            console.log('Price updated successfully:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
