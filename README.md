# tpconsole #

tpconsole is a small TypePad api client for use in python scripts.

You can install tpconsole using pip:

    pip install typepad
    pip install tpconsole


## Quick Start Guide ##


### Authentication ###

For many api calls, you will need to authenticate your script with TypePad.
tpconsole makes this easy by providing an `authenticate` function. For
example:

    import tpconsole

    tpconsole.authenticate()

During the authentication process, a browser window will be opened where you can
enter in your TypePad login credentials.  After logging in, you can close the
browser window.  Your script will continue executing in the background.


### More Authentication Options ###

By default, fbconsole will make all it's requests as the tpconsole TypePad app.
If you want the requests to be made by your own TypePad application, you must
modify the CONSUMER_KEY, CONSUMER_SECRET, APP_ID setting.  For example:

    tpconsole.CONSUMER_KEY = '<your-consumer-key>'
    tpconsole.CONSUMER_SECRET = '<your-consumer-secret>'
    tpconsole.APP_ID = '<your-app-id>'
    tpconsole.authenticate()

For the authentication flow to work, you must configure your TypePad
application correctly by setting the "URL" option to http://127.0.0.1:8080
on http://www.typepad.com/account/access/developer


### Other Options ###

There are two other options you can specify.

- `SERVER_PORT` controls which port the local server runs on.  If you modify
     this, make sure your applications settings on TypePad, specifically 
     "URL", reflect the port number you are using.  The default is 8080.

- `ACCESS_TOKEN_FILE` controls where the access token gets stored on the file
  system.  The default is `.tp_access_token`.


## Feedback ##

For issues pertaining to tpconsole only, use
[the issue tracker on github](https://github.com/saymedia/tpconsole/issues).
For issues with the TypePad JSON API or other aspects of TypePad's platform,
please refer to [the developer docs](http://www.typepad.com/services/apidocs)


## License Information ##

Based on fbconsole by Paul Carduner, Facebook
https://github.com/facebook/fbconsole

tpconsole is licensed under the [Apache License, Version
2.0](http://www.apache.org/licenses/LICENSE-2.0.html)
