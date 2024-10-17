$(document).ready(function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    $('#loginForm').on('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission
        const csrftoken = getCookie('csrftoken');
        // Gather form data
        const username = $('#username').val();
        const password = $('#password').val();  
        const repassword = $('#repassword').val();
        const useremail = $('#useremail').val();
      
        if (password === repassword) {

        $.ajax({
            url: 'http://127.0.0.1:8000/signup_view', // Backend endpoint for authentication
            type: 'POST', // HTTP method
            contentType: 'application/json', // Send as JSON
            headers: {
                'X-CSRFToken': csrftoken  // Include CSRF token in the request headers
            },
            data: JSON.stringify({ // Convert data to JSON
                username: username,
                password: password,
                email: useremail,
            }),
            success: function(response) {
                // Handle successful login
                alert('account created successful!');
                window.location.href = 'http://127.0.0.1:8000/dashboard';  // You can redirect or show a success message here
                // Example: window.location.href = '/dashboard'; // Uncomment this to redirect to dashboard
            },
            error: function(xhr) {
                // Handle error response
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    alert(xhr.responseJSON.message); // Show error message from response
                } else {
                    alert('account not created! create again');
                    window.location.href = 'http://127.0.0.1:8000/signup_page'; 
                     // Fallback error message
                }
            }
        });
    }else{
        $('#check').text('enter same password!');
    }

    });
});
