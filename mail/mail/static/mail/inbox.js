document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  document.querySelector('#back-button').addEventListener('click', () => {
    load_mailbox('inbox')
  });
  
  send_email();

  // Load the inbox by default
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

function send_email() {
  const form = document.querySelector('#compose-form');
  
  form.onsubmit = function() {
    // Get the values from the compose fields
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    
    // Send the email using fetch API
    fetch('/emails', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })

    .then(response => response.json())
    .then(result => {
      console.log(result);
      load_mailbox('sent');

    })

    .catch(error => {
      console.log('Error:', error);
    });
    
    return false;
  };
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get the emails for the selected mailbox
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Container for emails
      const emailsContainer = document.createElement('div');
      emailsContainer.id = 'emails-container';

      // Loop through each email and create a list item
      emails.forEach(email => {
        const emailElement = document.createElement('div');
        emailElement.className = `email ${email.read ? 'read' : 'unread'}`;
        
        // Add email content
        emailElement.innerHTML = `
          <div class="email-sender">${email.sender}</div>
          <div class="email-subject">${email.subject}</div>
          <div class="email-timestamp">${email.timestamp}</div>
        `;
        // Add click event to view the email
        emailElement.addEventListener('click', () => view_email(email.id));
        
        // Append the email item to the emails view
        emailsContainer.appendChild(emailElement);
      });
      // Add emails to the DOM  
      document.querySelector('#emails-view').appendChild(emailsContainer);
    })
    .catch(error => {
      console.error('Error loading mailbox:', error);
      document.querySelector('#emails-view').innerHTML = 
        `<p class="error">Error loading ${mailbox} mailbox. Please try again.</p>`;
    });
}

function view_email(email_id) {
  // Hide other views and show email view
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // Get the email
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      // Display email
      document.querySelector('#email-sender').innerHTML = email.sender;
      document.querySelector('#email-recipients').innerHTML = email.recipients.join(', ');
      document.querySelector('#email-subject').innerHTML = email.subject;
      document.querySelector('#email-timestamp').innerHTML = email.timestamp;
      document.querySelector('#email-body').innerHTML = email.body;

      // Mark as read if it isn't already
      if (!email.read) {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        });
      }

      // Set up reply button
      document.querySelector('#reply-button').onclick = () => {
        compose_email('reply', email);
      };
    })
    .catch(error => {
      console.error('Error loading email:', error);
      document.querySelector('#email-view').innerHTML = 
        '<p class="error">Error loading email. Please try again.</p>';
    });
}