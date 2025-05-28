document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#back-button').addEventListener('click', () => load_mailbox('inbox'));

  // Set up form submission handler
  send_email();

  // Load the inbox by default
  load_mailbox('inbox');
});

function showAlert(message, type = 'success') {
  const alertDiv = document.createElement('div');
  alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
  alertDiv.role = 'alert';
  alertDiv.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  
  // Insert at the top of the body
  document.body.prepend(alertDiv);
  
  // Remove after 3 seconds
  setTimeout(() => alertDiv.remove(), 3000);
}

function compose_email(action = 'new', email = null) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  const recipients = document.querySelector('#compose-recipients');
  const subject = document.querySelector('#compose-subject');
  const body = document.querySelector('#compose-body');

  recipients.value = '';
  subject.value = '';
  body.value = '';

  if (action === 'reply') {
    recipients.value = email.sender;
    subject.value = email.subject.startsWith('Re: ') 
      ? email.subject 
      : `Re: ${email.subject}`;
    body.value = `\n\nOn ${email.timestamp}, ${email.sender} wrote:\n${email.body}`;
  }
}

function send_email() {
  const form = document.querySelector('#compose-form');
  
  form.onsubmit = function(e) {
    e.preventDefault();
    
    // Get the values from the compose fields
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    
    // Show loading state
    const submitBtn = form.querySelector('[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.value = 'Sending...';
    
    // Send the email
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
    .then(response => {
      if (!response.ok) {
        return response.json().then(err => { throw err; });
      }
      return response.json();
    })
    .then(result => {
      showAlert('Email sent successfully!');
      load_mailbox('sent');
    })
    .catch(error => {
      console.error('Error:', error);
      showAlert(error.error || 'Failed to send email', 'danger');
    })
    .finally(() => {
      submitBtn.disabled = false;
      submitBtn.value = 'Send';
    });
    
    return false;
  };
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show loading state
  document.querySelector('#emails-view').innerHTML = `
    <h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>
    <div class="text-center my-4">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  `;

  // Get the emails for the selected mailbox
  fetch(`/emails/${mailbox}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to load emails');
      }
      return response.json();
    })
    .then(emails => {
      // Clear loading state
      document.querySelector('#emails-view').innerHTML = `
        <h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>
      `;

      if (emails.length === 0) {
        document.querySelector('#emails-view').innerHTML += `
          <div class="alert alert-info">No emails in this mailbox</div>
        `;
        return;
      }

      // Container for emails
      const emailsContainer = document.createElement('div');
      emailsContainer.id = 'emails-container';
      emailsContainer.className = 'list-group';

      // Loop through each email
      emails.forEach(email => {
        const emailElement = document.createElement('a');
        emailElement.className = `list-group-item list-group-item-action ${email.read ? 'read' : 'unread'}`;
        
        emailElement.innerHTML = `
          <div class="d-flex w-100 justify-content-between">
            <h6 class="mb-1">${email.sender}</h6>
            <small>${email.timestamp}</small>
          </div>
          <p class="mb-1">${email.subject}</p>
          <small class="text-muted">${email.body.substring(0, 100)}...</small>
        `;
        
        emailElement.addEventListener('click', () => view_email(email.id));
        emailsContainer.appendChild(emailElement);
      });
      
      document.querySelector('#emails-view').appendChild(emailsContainer);
    })
    .catch(error => {
      console.error('Error:', error);
      document.querySelector('#emails-view').innerHTML = `
        <h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>
        <div class="alert alert-danger">
          Failed to load emails. Please try again.
        </div>
      `;
    });
}

function view_email(email_id) {
  // Hide other views and show email view
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // Show loading state
  document.querySelector('#email-view').innerHTML = `
    <div class="text-center my-4">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  `;

  // Get the email
  fetch(`/emails/${email_id}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to load email');
      }
      return response.json();
    })
    .then(email => {
      // Display email
      document.querySelector('#email-view').innerHTML = `
        <div class="email-header">
          <div><strong>From:</strong> <span id="email-sender">${email.sender}</span></div>
          <div><strong>To:</strong> <span id="email-recipients">${email.recipients.join(', ')}</span></div>
          <div><strong>Subject:</strong> <span id="email-subject">${email.subject}</span></div>
          <div><strong>Timestamp:</strong> <span id="email-timestamp">${email.timestamp}</span></div>
        </div>
        <hr>
        <div id="email-body" class="email-body">${email.body}</div>
        <button id="reply-button" class="btn btn-primary mt-3">Reply</button>
        <button id="back-button" class="btn btn-secondary mt-3">Back</button>
      `;

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

      // Add archive/unarchive button
      const archiveBtn = document.createElement('button');
      archiveBtn.className = `btn btn-sm mt-3 me-2 ${email.archived ? 'btn-success' : 'btn-warning'}`;
      archiveBtn.textContent = email.archived ? 'Unarchive' : 'Archive';
      
      archiveBtn.addEventListener('click', () => {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: !email.archived
          })
        })
        .then(() => {
          showAlert(`Email ${email.archived ? 'unarchived' : 'archived'} successfully!`);
          load_mailbox('inbox');
        })
        .catch(error => {
          console.error('Error:', error);
          showAlert('Failed to update email status', 'danger');
        });
      });

      document.querySelector('#reply-button').before(archiveBtn);
    })
    .catch(error => {
      console.error('Error:', error);
      document.querySelector('#email-view').innerHTML = `
        <div class="alert alert-danger">
          Failed to load email. Please try again.
        </div>
        <button id="back-button" class="btn btn-secondary mt-3">Back</button>
      `;
    });
}