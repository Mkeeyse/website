// Get the profile link and main section
const profileLink = document.getElementById('profile-link');
const mainSection = document.getElementById('main-section');

// Add click event listener to the profile link
profileLink.addEventListener('click', displayUserProfile);

// Function to display the user profile in the main section
function displayUserProfile(event) {
  event.preventDefault();

  // Clear the main section
  mainSection.innerHTML = '';

  // Create user profile elements
  const heading = document.createElement('h1');
  heading.textContent = 'User Profile';

  const username = document.createElement('p');
  username.innerHTML = `<strong>Username:</strong> ${user_info.username}`;

  const email = document.createElement('p');
  email.innerHTML = `<strong>Email:</strong> ${user_info.email}`;

  const department = document.createElement('p');
  department.innerHTML = `<strong>Department:</strong> ${user_info.department}`;

  // Append elements to the main section
  mainSection.appendChild(heading);
  mainSection.appendChild(username);
  mainSection.appendChild(email);
  mainSection.appendChild(department);
}
