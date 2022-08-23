# 2factor authentication app

## .env example

Please create `backend/.env` file and pass all data listed below there. They are needed for proper application work. If you want to test it with email sender (WORKS ONLY WITH GMAIL) set `SEND_EMAIL=1` and ensure that your gmail account is set up with 3rd party applications.

```
MAIL_USERNAME=<your-email-for-testing>
MAIL_FROM=<your-email-for-testing>
MAIL_PASSWORD=<your-mail-password>
SEND_MAIL=0
```

## Run app

Start docker on your machine and in main directory run `docker-compose up --build`.

# Users

If you configured everything properly you should be able to login with 2 accounts.
First account with OTP enabled is 
```
login = <your email passed in .env>
password = zaq1@WSX
```
If you set SEND_MAIL value to 0 just type `11111` in verification code page.

Otherwise check your mailbox and type given code. 

To log in into second account (without OTP) use:
```
login = test2@mail.com
password = 123$%^QWE
```
