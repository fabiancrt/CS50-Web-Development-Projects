// hello there cs50 team , my name is Fabian Cretu and I want yo thank you guys for taking your time to review my completion of the starting project that..
// you guys have provided

//here is the default given code
//default domcontentloaded
document.addEventListener('DOMContentLoaded', function() {
    // Use buttons to toggle between views(given by default)
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    //extra spam button
    document.querySelector('#spam').addEventListener('click', () => load_mailbox('spam'));
    document.querySelector('#compose').addEventListener('click', compose_email);
  
    // By default, load the inbox(given by default)
    load_mailbox('inbox');
  });
  
  //edited loadmailbox function from the provided one
  function load_mailbox(mailbox) {
    // Show the mailbox and hide other views(this is by default)
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    //i added this queryselector to hide the requested email display
    document.querySelector('#email-view').style.display = 'none';
  
    // Show the mailbox name (this is by default)
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
    // fettching emails for the mailbox (implemented with the help of the examples you guys provided)
    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {
            // here is the part where the emails get displayed (also used for each like the hints pointed out) v
            emails.forEach(email => {
                const emailDiv = document.createElement('div');
                // also implemented the read or unread feature the team requested 
                emailDiv.className = `email ${email.read ? 'read' : 'unread'}`;
                emailDiv.innerHTML = `
                    <span class="sender">${mailbox === 'sent' ? 'To: ' + email.recipients.join(', ') : email.sender}</span>
                    <span class="subject">${email.subject}</span>
                    <span class="timestamp">${email.timestamp}</span>
                `;
                emailDiv.addEventListener('click', () => view_email(email.id, mailbox));
                document.querySelector('#emails-view').append(emailDiv);
            });
        });
  }
  //this is the modified emailcompose function started from the default one
  function compose_email() {
    // Show compose view and hide other views(default given)
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    //same as before added the queryselectoor for the email display
    document.querySelector('#email-view').style.display = 'none';
  
    // Clear out composition fields(displayed by)
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  
    // this is where code modifications made start , here is where the form subissions are handeled like the post/email example the team provided
    document.querySelector('#compose-form').onsubmit = function() {
        const recipients = document.querySelector('#compose-recipients').value;
        const subject = document.querySelector('#compose-subject').value;
        const body = document.querySelector('#compose-body').value;
      //inspired from the given example  on the site
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
            // after the email is sent , this opens up the sent mails
            load_mailbox('sent');
        });
  
        return false;
    };
  }
  //this is the function for the view email that is requested by the team and that i added
  function view_email(email_id, mailbox) {
    // made similar structure like you guys provided in the examples
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
  
    // email fetching guided by the previous code
    fetch(`/emails/${email_id}`)
        .then(response => response.json())
        .then(email => {
            // the details requested here: Your application should show the email’s sender, recipients, subject, timestamp, and body.
            document.querySelector('#email-view').innerHTML = `
                <div><strong>From:</strong> ${email.sender}</div>
                <div><strong>To:</strong> ${email.recipients.join(', ')}</div>
                <div><strong>Subject:</strong> ${email.subject}</div>
                <div><strong>Timestamp:</strong> ${email.timestamp}</div>
                <hr>
                <div>${email.body}</div>
            `;
  
            // here is where the email is read/undread using the put method : "Recall that you can send a PUT request to /emails/<email_id> to update whether an email is read or not."
            if (!email.read) {
                fetch(`/emails/${email_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({ read: true })
                })
                .then(() => {
                    const emailElement = document.querySelector(`#email-${email_id}`);
                    if (emailElement) {
                        emailElement.classList.remove('unread');
                        emailElement.classList.add('read');
                    }
                });
            }
  
            // now the archive and unarchived button to make the function work , similar put method used like on the website
            //also if the user does not access the email through the sent tab (emails that are sent should not have reply and archive buttons) then buttons will appear
            // as extra content i added the spam feature similar to the archive one but i added a count function in views that counts emails sent from
            //the same user in the same day and if that number surpasses 10 then emails automatically get sent to spam
            if (mailbox !== 'sent') {
                const spamButton = document.createElement('button');
                spamButton.innerHTML = email.spam  ? 'Unmark Spam' : 'Mark Spam';
                spamButton.addEventListener('click', () => {
                    fetch(`/emails/${email_id}`, {
                        method: 'PUT',
                        body: JSON.stringify({ spam : !email.spam })
                    })
                    .then(() => load_mailbox('inbox'));
                });
                document.querySelector('#email-view').append(spamButton);

                const archiveButton = document.createElement('button');
                archiveButton.innerHTML = email.archived ? 'Unarchive' : 'Archive';
                archiveButton.addEventListener('click', () => {
                    fetch(`/emails/${email_id}`, {
                        method: 'PUT',
                        body: JSON.stringify({ archived: !email.archived })
                    })
                    .then(() => load_mailbox('inbox'));
                });
                document.querySelector('#email-view').append(archiveButton);
  
                // & finally the requested reply button that also has the pre-fill funcctions that are specified :Pre-fill the subject line. 
                //If the original email had a subject line of foo, the new subject line should be Re: foo. 
                //(If the subject line already begins with Re: , no need to add it again.)
                //Pre-fill the body of the email with a line like "On Jan 1 2020, 12:00 AM foo@example.com wrote:" followed by the original text of the email.
                const replyButton = document.createElement('button');
                replyButton.innerHTML = 'Reply';
                replyButton.addEventListener('click', () => {
                    compose_email();
                    document.querySelector('#compose-recipients').value = email.sender;
                    document.querySelector('#compose-subject').value = email.subject.startsWith('Re:') ? email.subject : `Re: ${email.subject}`;
                    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}\n`;
                });
                document.querySelector('#email-view').append(replyButton);
            }
        });
  }
  
  //& also in my css i incorporated the necessary css so that emails are grey if read and white if not read
  //besides the required css i addes some css to make the website look better
  //you can see my css in the css file but to make it simple for you guys i will also leave it here:
  //.email.unread {
  //  background-color: white;
  //  }
  
  //.email.read {
  //  background-color: rgba(209, 193, 190, 0.372)
  //  }