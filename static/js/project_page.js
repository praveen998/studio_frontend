
function previous_page(){
    window.location.href = 'http://127.0.0.1:5000/show_projects'; 
}

$(document).ready(function() {

    $.ajax({
        url: 'http://127.0.0.1:5000/check_images_uploaded', // Backend endpoint for authentication
        type: 'GET', // HTTP method
        success: function(response) {
            // Handle successful login
            //alert('folder is empty');
            $('#uploadbox').show();
          //  window.location.href = 'http://127.0.0.1:5000/';  // You can redirect or show a success message here
            // Example: window.location.href = '/dashboard'; // Uncomment this to redirect to dashboard
        },
        error: function(xhr) {
            // Handle error response
            if (xhr.responseJSON && xhr.responseJSON.message) {
                alert(xhr.responseJSON.message); // Show error message from response
            } else {
                ///alert('folder is not empty');
                $('#uploadbox').hide();
                //window.location.href = 'http://127.0.0.1:5000/'; 
                 // Fallback error message
            }
        }
    });
});

