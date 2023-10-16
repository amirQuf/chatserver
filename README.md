# Chatserver
A client chat server that is using **tcp socket**  to  connect  to __server__ and sending message to server and get response.
we can send __private message__  or __public message__. 
## Libraries:
- Socket
- re
- datetime
- threading

## How to run?
- **frist step** : run `server.py`.<br>
  ```Python3 server.py```
- **second step** :run `clien.py`.<br>
    ```Python3 client.py```
creating viritual enviorment is not obligatory.

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
   
