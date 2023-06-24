const profileLink = document.getElementById('profile-link');
const mainSection = document.getElementById('main-section');

profileLink.addEventListener('click', displayUserProfile);

function displayUserProfile(event) {
  event.preventDefault();

  mainSection.innerHTML = '';

  const container = document.createElement('div');
  container.style.border = '1px solid #ccc';
  container.style.padding = '20px';
  container.style.margin = '0 auto';
  container.style.width = '400px';
  container.style.display = 'flex';
  container.style.flexDirection = 'column';
  container.style.alignItems = 'center';
  container.style.marginLeft = '12px'; // Add this line to set left margin
  container.style.marginRight = 'auto'; // Add this line to set right margin

  const profileAvatar = document.createElement('div');
  profileAvatar.style.textAlign = 'center';

  const avatarImg = document.createElement('img');
  avatarImg.src = 'static/pictures/people.png'; // Replace with the actual path to the profile avatar image
  avatarImg.alt = 'Profile Avatar';
  avatarImg.style.width = '150px';
  avatarImg.style.height = '150px';
  avatarImg.style.borderRadius = '50%';
  avatarImg.style.objectFit = 'cover';
  avatarImg.style.border = '2px solid #ccc';

  profileAvatar.appendChild(avatarImg);

  const infoContainer = document.createElement('div');

  const department = document.createElement('p');
  department.innerHTML = `<strong>Department:</strong> ${user_info.department}`;
  department.style.borderBottom = '1px solid #ccc';
  department.style.paddingBottom = '5px';

  const email = document.createElement('p');
  email.innerHTML = `<strong>Email:</strong> ${user_info.email}`;
  email.style.borderBottom = '1px solid #ccc';
  email.style.paddingBottom = '5px';

  const username = document.createElement('p');
  username.innerHTML = `<strong>Username:</strong> ${user_info.username}`;
  username.style.borderBottom = '1px solid #ccc';
  username.style.paddingBottom = '5px';

  infoContainer.appendChild(department);
  infoContainer.appendChild(email);
  infoContainer.appendChild(username);

  container.appendChild(profileAvatar);
  container.appendChild(infoContainer);

  mainSection.appendChild(container);
}
