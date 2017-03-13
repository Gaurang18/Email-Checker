
import datetime
import email
import imaplib
import mailbox

# mail = imaplib.IMAP4_SSL('imap.gmail.com')
# mail.login('gaurangbansal18@gmail.com', 'madanmohan1')
# mail.list()
# mail.select('inbox')

# #need to add some stuff in here
# mail.select('inbox')
# typ, data = mail.search(None, 'ALL')
# ids = data[0]
# id_list = ids.split()
# #get the most recent email id
# ip = len(data[0].split())
# print ip
# latest_email_id = int( id_list[-1] )

# #iterate through 15 messages in decending order starting with latest_email_id
# #the '-1' dictates reverse looping order
# for i in range( latest_email_id, latest_email_id-ip, -1 ):
# #for i in range(ip):
#    typ, data = mail.fetch( i, '(RFC822)' )
#    #latest_email_uid = data[0].split()[i]
#    #typ, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
#    #print data
#    for response_part in data:
#       if isinstance(response_part, tuple):
#           msg = email.message_from_string(response_part[1])
#           varSubject = msg['subject']
#           varFrom = msg['from']
#    #remove the brackets around the sender email address
#    varFrom = varFrom.replace('<', '')
#    varFrom = varFrom.replace('>', '')

#    #add ellipsis (...) if subject length is greater than 35 characters
#    # if len( varSubject ) > 35:
#    #    varSubject = varSubject[0:32] + '...'

#    print '[' + varFrom.split()[-1] + '] ' + varSubject

# mail.logout()




EMAIL_ACCOUNT = "gaurangbansal18@gmail.com"
PASSWORD = "madanmohan1"

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(EMAIL_ACCOUNT, PASSWORD)
mail.list()
mail.select('inbox')
result, data = mail.uid('search', None, "ALL") # (ALL/UNSEEN)
i = len(data[0].split())

for x in range(i):
    latest_email_uid = data[0].split()[x]
    result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    # result, email_data = conn.store(num,'-FLAGS','\\Seen') 
    # this might work to set flag to seen, if it doesn't already
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    # Header Details
    date_tuple = email.utils.parsedate_tz(email_message['Date'])
    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
    email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
    email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
    subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
    d = email_from.split(" ")
    # email_z = d[1] + d[2]
    # Body details
    e = local_message_date.split(" ")
    f = e[1] +" " + e[2] + " " + e[3]
    for part in email_message.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True)
            #file_name = str(x) + ". "+ d[0]+ ".txt"
            file_name = d[0]+" "+f+ ".txt"
            output_file = open(file_name, 'w')
            output_file.write("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" %(email_from, email_to,local_message_date, subject, body.decode('utf-8')))
            output_file.close()
        else:
            continue