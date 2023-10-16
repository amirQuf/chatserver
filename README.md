# Chat server

A client chat server that is using **tcp socket** to connect to **server** and sending message to server and get response with especial protocol.

we can send **private message** or **public message**.

## Libraries:

- Socket
- re
- datetime
- threading

## How to run?

**step #1** : run `server.py`.

      ```Python3 server.py```

**step #2** :run `client.py`.

      ```Python3 client.py```

creating virtual environment is not obligatory.

## How to send message:

1.Hello `<user_name>`.<br>
2.Please send the list of attendees. <br>
3.Public message, length=`<message_len>`:<br>
`<message_body>` <br>
4.Private message, length=`<message_len>` to `<user_name1>`,`<user_name2>`,`<user_name3>`,`<user_name4>`:
`<message_body>`<br>
5.Bye.

#### ToDO:

- [ ] cleaning codes
- [ ] use log
