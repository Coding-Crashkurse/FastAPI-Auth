import os
import smtplib
from email.message import EmailMessage

email = os.getenv("email")
password = os.getenv("password")


def send_mail(to, token, username, email=email, password=password):
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
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(email, password)
    server.send_message(msg)
    server.quit()
