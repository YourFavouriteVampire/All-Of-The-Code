// Get the modal element
var modal = document.getElementById("modal");

// Get the buttons that open the modal
var loginBtn = document.getElementById("loginBtn");
var signupBtn = document.getElementById("signupBtn");

// Get the close button element
var closeBtn = document.getElementsByClassName("close")[0];

// Function to open the modal
function openModal() {
  modal.style.display = "block";
}

// Function to close the modal
function closeModal() {
  modal.style.display = "none";
}

// Event listeners for the login and sign-up buttons
loginBtn.addEventListener("click", function() {
  openModal();
  document.getElementById("signupForm").style.display = "none";
  document.getElementById("loginForm").style.display = "block";
});

signupBtn.addEventListener("click", function() {
  openModal();
  document.getElementById("loginForm").style.display = "none";
  document.getElementById("signupForm").style.display = "block";
});

// Event listener for the close button
closeBtn.addEventListener("click", closeModal);

// Event listener to close the modal when clicking outside of it
window.addEventListener("click", function(event) {
  if (event.target == modal) {
    closeModal();
  }
});
