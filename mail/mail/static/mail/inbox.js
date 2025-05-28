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
    },
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => {
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
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}