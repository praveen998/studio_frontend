$(document).ready(function() {
    $('#loginForm').on('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission

        // Gather form data
        const username = $('#username').val();
        const password = $('#password').val();

        $.ajax({
            url: 'http://127.0.0.1:5000/login_auth', // Backend endpoint for authentication
            type: 'POST', // HTTP method
            contentType: 'application/json', // Send as JSON
            data: JSON.stringify({ // Convert data to JSON
                username: username,
                password: password
            }),
            success: function(response) {
                // Handle successful login
                alert('Login successful!');
                window.location.href = 'http://127.0.0.1:5000/';  // You can redirect or show a success message here
                // Example: window.location.href = '/dashboard'; // Uncomment this to redirect to dashboard
            },
            error: function(xhr) {
                // Handle error response
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    alert(xhr.responseJSON.message); // Show error message from response
                } else {
                    alert('An unexpected error occurred.');
                    window.location.href = 'http://127.0.0.1:5000/login'; 
                     // Fallback error message
                }
            }
        });
    });
});
