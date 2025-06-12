document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Handle the send email button
  document.querySelector('#compose-form').onsubmit = function(event) {
    send_email(event);
  }
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


// Function to view the details of an email
function view_email(email_id) {
  
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch the emails for the selected mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Showing each email in the mailbox inside a div
    emails.forEach(email => {
      console.log(email);

      const newEmail = document.createElement('div');
      newEmail.className = 'list-group-item';
      newEmail.style.cursor = 'pointer';
      newEmail.style.border = '1px solid #ccc';
      newEmail.style.padding = '10px';
      newEmail.style.marginBottom = '10px';
      newEmail.innerHTML = `
        <strong>From:</strong> ${email.sender} <br>
        <strong>Subject:</strong> ${email.subject} <br>
        <strong>Timestamp:</strong> ${email.timestamp} <br>      
      `;

      // Change the background color based on read status
      if (email.read) {
        newEmail.style.backgroundColor = '#E0E0E0'; // Light gray for read emails
      } else if (email.unread) {
        newEmail.style.backgroundColor = '#ffffff'; // White for unread emails
      }
      // Adding event listener to each email so when clicked its details are shown
       newEmail.addEventListener('click', function() {
        // Showing the email view and hiding other views
        document.querySelector('#email-view').style.display = 'block';
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
        view_email(email.id);
      });
    document.querySelector('#emails-view').append(newEmail);
    });
  });
}

// Function to send the emails
function send_email(event) {
  
  // Prevent the default form submission behavior
  event.preventDefault();

  // Getting the values from the compose form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Sending email via a POST request 
  fetch('/emails', {
    method: 'POST', 
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  
  .then(response => response.json())
  .then(result => {
    console.log(result);
    load_mailbox('sent'); // Load the sent mailbox after sending the email
  })

  // Catch errors in the fetch request
  .catch(error => {
    console.error('Error:', error);
  });
}