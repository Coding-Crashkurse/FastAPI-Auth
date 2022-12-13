import os
import smtplib
from email.message import EmailMessage
from fastapi import requests

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
API_KEY = os.getenv("MAILGUN_API_KEY")


def send_mail(to, token, username, email=EMAIL, password=PASSWORD):
    msg = EmailMessage()
    msg.add_alternative(
        f"""\
<html>
  <head>

    <title>Document</title>
  </head>
  <body>
    <div id="box">
      <h2>Hallo {username},</h2> 
        <p> Bevor du die Seite nutzen kannst, klicke 
            <a href="http://localhost:8000/verify/{token}">
                hier
            </a> um deine registrierung zu bestätigen
        </p>
      </form>
    </div>
  </body>
</html>

<style>
  #box {{
    margin: 0 auto;
    max-width: 500px;
    border: 1px solid black;
    height: 200px;
    text-align: center;
    background: lightgray;
  }}

  p {{
    padding: 10px 10px;
    font-size: 18px;
  }}

  .inline {{
    display: inline;
  }}

  .link-button {{
    background: none;
    border: none;
    color: blue;
    font-size: 22px;
    text-decoration: underline;
    cursor: pointer;
    font-family: serif;
  }}
  .link-button:focus {{
    outline: none;
  }}
  .link-button:active {{
    color: red;
  }}
</style>
    """,
        subtype="html",
    )

    msg["Subject"] = "Bestätigung deiner Registrierung"
    msg["From"] = email
    msg["To"] = to

    # Send the message via our own SMTP server.
    server = smtplib.SMTP("smtp.mailgun.org", 587)
    server.login(email, password)
    server.send_message(msg)
    server.quit()


# def send_mail(to, token, username, email=email, password=password):
# 	return requests.post(
# 		"https://api.mailgun.net/v3/sandboxf9238eb2a4d644789ba080fd0bcaa64e.mailgun.org",
# 		auth=("api", API_KEY),
# 		data={"from": "Excited User <mailgun@YOUR_DOMAIN_NAME>",
# 			"to": ["bar@example.com", "YOU@YOUR_DOMAIN_NAME"],
# 			"subject": "Hello",
# 			"text": "Testing some Mailgun awesomness!"})