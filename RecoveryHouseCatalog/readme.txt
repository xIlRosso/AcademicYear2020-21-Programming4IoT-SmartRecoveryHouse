Prerequisites:
install the package pyngrok


How to startup the catalog as a public ip address:

Open a command prompt and on windows write the following command:

taskkill /f /im ngrok.exe

Run main.py file (this is the cherrypy server)
In another terminal run setup_ngrok

The program publishes 1000 times the public address of the server
This is because every time somebody subscribes and downloads a message that
message is dequeued from the broker so just to make sure that
every part of the ecosystem gets the public address