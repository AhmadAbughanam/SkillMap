// Wait for the DOM to be fully loaded before running scripts
document.addEventListener('DOMContentLoaded', function () {

  // 1. Add confirmation dialogs to all delete forms
  // This script looks for any form with the class "confirm-delete"
  const deleteForms = document.querySelectorAll('.confirm-delete');
  deleteForms.forEach(form => {
    form.addEventListener('submit', function (event) {
      // Prevent the form from submitting immediately
      event.preventDefault();
      
      // Show a confirmation dialog
      const userConfirmed = confirm('Are you sure you want to delete this item? This action cannot be undone.');
      
      // If the user clicked "OK", submit the form
      if (userConfirmed) {
        this.submit();
      }
    });
  });

  // 2. Set the active link in the navigation bar
  // This helps users know which page they are currently on.
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
  
  navLinks.forEach(link => {
    // Check if the link's href attribute matches the current page's path
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // 3. Initialize Bootstrap Tooltips
  // This will enable tooltips for any element that has the `data-bs-toggle="tooltip"` attribute.
  // This is a proactive addition for future enhancements.
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

});
