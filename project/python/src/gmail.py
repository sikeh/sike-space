import smtplib

fromaddr = 'sike.huang@gmail.com'
toaddrs = 'sike.huang@live.com'

msg = 'hello world'

username = 'sike.huang@gmail.com'
password = 'password'

server = smtplib.SMTP(host='smtp.gmail.com', port=587)
server.ehlo()
server.starttls()
server.ehlo()
server.login(username, password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()

