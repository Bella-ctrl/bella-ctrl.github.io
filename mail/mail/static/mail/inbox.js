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

function send_email(event) {  
  event.preventDefault(); 
  console.log("Email send initiated");
  
  // Get values from the form fields
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

  console.log("Sending to:", recipients);
  
  // Send POST request
  fetch('/emails', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrf,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => {
    console.log('Response status:', response.status);
    return response.json().then(data => ({
      status: response.status,
      data
    }));
  })
  .then(({status, data}) => {
    console.log('Full response:', data);
    if (status === 201) {
      load_mailbox('sent');
    } else {
      throw new Error(data.error || 'Email sending failed');
    }
  })
  .catch(error => {
    console.error('Error details:', error);
    alert('Error: ' + error.message);
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
