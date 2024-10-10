function folderClick(projectName) {
  $.ajax({
    url: 'http://127.0.0.1:5000/project_page', 
    type: 'POST',
    data: { "project_name": projectName }, 
    success:function(response){
      window.location.href = 'http://127.0.0.1:5000/project_page_render'; 
    },

});
}


$(document).ready(function() {
  $.ajax({
    url: 'http://127.0.0.1:5000/project_names',
    type: 'GET',          
    dataType: 'json',     
    success: function(response) {
      $.each(response, function(index, project) {
        $('#folder-data').append(`
          <div class="col-md-3 mb-2">
              <div class="card-body d-flex align-items-center">
                <img src="../static/images/folder.png" alt="Folder Icon" class="icon" onclick="folderClick('${project}')">
                <h5 class="card-title mb-0">${project}</h5>
              </div>
          </div>
        `);
      });
    }
  });

  
 $('#projectForm').on('submit', function(e) {
      e.preventDefault(); 
      $.ajax({
          url: 'http://127.0.0.1:5000/create_project',
          type: 'POST', 
          data: $(this).serialize(),  
          success: function(response) {
              alert(response.message);
              window.location.href = 'http://127.0.0.1:5000/'; 
          },
          error: function(xhr) {
            alert('An unexpected error occurred.'); 
            window.location.href = 'http://127.0.0.1:5000/';
          }
      });
    });
});
