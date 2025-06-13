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
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function view_email(email_id) {
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);

    // Showing the email view and hiding other views
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    
    // Show Email Details
    document.querySelector('#email-view').innerHTML = `
      <strong>From:</strong> ${email.sender} <br>
      <strong>To:</strong> ${email.recipients} <br>  
      <strong>Subject:</strong> ${email.subject} <br>
      <strong>Timestamp:</strong> ${email.timestamp} <br>
      <div class="card"><div class="card-body">${email.body}</div></div>
      `;
    
    // Mark email as read
    if (!email.read) {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    }

    // Show Archive/Unarchive button only for inbox or archive (Not Sent)
    const currentMailbox = window.location.hash.substring(1);
    if (currentMailbox !== 'sent') {
      const buttonArc = document.createElement('button');
      buttonArc.className = 'btn btn-outline-dark';
      buttonArc.style.marginTop = '2px';
      buttonArc.style.marginRight = '5px';
      
      // Show "Archive" for inbox, "Unarchive" for archive
      buttonArc.innerHTML = currentMailbox === 'inbox' ? "Archive" : "Unarchive";
      
      buttonArc.addEventListener('click', function() {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: currentMailbox === 'inbox' // Archive if from inbox, unarchive if from archive
          })
        })
        .then(() => { load_mailbox('inbox') }); // Always return to inbox after
      });
      document.querySelector('#email-view').append(buttonArc);
    }
  
    // Reply Button (unchanged)
    const buttonRep = document.createElement('button');
    buttonRep.className = 'btn btn-outline-dark';
    buttonRep.innerHTML= "Reply";

    buttonRep.addEventListener('click', function() {
      console.log("reply")
      compose_email();

      // Populate compose fields
      document.querySelector('#compose-recipients').value = email.sender;
      let subject = email.subject;
      if (subject.split(' ',1)[0] != "Re:") {
        subject = "Re: " + email.subject;
      }
      document.querySelector('#compose-subject').value = subject;
      document.querySelector('#compose-body').value = `"On ${email.timestamp}, ${email.sender} wrote: ${email.body}"`;
    });
    document.querySelector('#email-view').append(buttonRep);
  });
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Update URL hash to track current mailbox
  window.location.hash = mailbox;

  // Fetch the emails for the selected mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Showing each email in the mailbox inside a div
    emails.forEach(email => {
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
      } else {
        newEmail.style.backgroundColor = '#ffffff'; // White for unread emails
      }
      
      // Adding event listener to each email
      newEmail.addEventListener('click', function() {
        view_email(email.id);
      });
      document.querySelector('#emails-view').append(newEmail);
    });
  });
}

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
    load_mailbox('sent');
  })
  
  .catch(error => {
    console.error('Error:', error);
  });
}