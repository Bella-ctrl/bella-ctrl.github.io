document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Connect the form to the send_email function
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Handle email form submission
  document.querySelector('#compose-form').addEventListener('submit', send_email);
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

<<<<<<< HEAD
function send_email(event) {  
  event.preventDefault(); 
  
  // Get values from the form fields
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // Debug: Log the values before sending
  console.log('Attempting to send:', {recipients, subject, body});

  // Send POST request
  fetch('/emails', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrf,
      'Content-Type': 'application/json'
=======
function send_email(event) {
  event.preventDefault();
  
  // Get values from form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send email via API
  fetch('/emails', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/json',
>>>>>>> 959123a2e6f140860607eb2663fed5b12c99a8aa
    },
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => {
<<<<<<< HEAD
    console.log('Received response status:', response.status);
    if (!response.ok) {
      // Get the error message if exists
      return response.json().then(err => { 
        throw new Error(err.error || 'Unknown error');
      });
    }
    return response.json();
  })
  .then(data => {
    console.log('Success:', data);
    load_mailbox('sent'); // Use your existing function
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Error: ' + error.message); // Show actual error message
=======
    if (response.status !== 201) {
      return response.json().then(error => { throw new Error(error.error); });
    }
    return response.json();
  })
  .then(result => {
    console.log(result);
    // Load the sent mailbox after successful send
    load_mailbox('sent');
  })
  .catch(error => {
    console.error('Error:', error);
    alert(error.message);
>>>>>>> 959123a2e6f140860607eb2663fed5b12c99a8aa
  });
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Load the emails for this mailbox
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      if (Array.isArray(emails)) {
        // Create a container for emails
        const emailsContainer = document.createElement('div');
        emailsContainer.className = 'emails-container';
        
        // Add each email to the container
        emails.forEach(email => {
          const emailElement = document.createElement('div');
          emailElement.className = `email ${email.read ? 'read' : 'unread'}`;
          emailElement.innerHTML = `
            <div class="email-sender">${email.sender}</div>
            <div class="email-subject">${email.subject}</div>
            <div class="email-timestamp">${email.timestamp}</div>
          `;
          emailElement.addEventListener('click', () => view_email(email.id));
          emailsContainer.appendChild(emailElement);
        });
        
        // Add container to the view
        document.querySelector('#emails-view').appendChild(emailsContainer);
      } else {
        console.error('Unexpected response:', emails);
      }
    })
    .catch(error => console.error('Error loading emails:', error));
}

function view_email(email_id) {
  // Fetch the email
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      // Display the email
      document.querySelector('#emails-view').innerHTML = `
        <div class="email-view">
          <div><strong>From:</strong> ${email.sender}</div>
          <div><strong>To:</strong> ${email.recipients.join(', ')}</div>
          <div><strong>Subject:</strong> ${email.subject}</div>
          <div><strong>Timestamp:</strong> ${email.timestamp}</div>
          <hr>
          <div class="email-body">${email.body}</div>
        </div>
      `;
      
      // Mark as read
      if (!email.read) {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            read: true
          })
        });
      }
    });
}

// Helper function to get CSRF token
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