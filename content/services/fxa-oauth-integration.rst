How we implemented a Firefox Account OAuth service provider with Cornice
########################################################################

:slug: fxa-oauth-integration
:date: 23-12-2014
:authors: Alexis Métaireau, Rémy Hubscher
:tags: FxA, python
:lang: en

Daybed is user agnostic, when you logs in you grab an Hawk Token
derives into credentials that are used to sign every request made to
the API.

This token can then be linked to anything: the user, the device or a
group with share credentials.

This lets people use daybed the way it fits their software.

Also when you want user's devices to use the same token, you need a way
to share it.


Get a token using Basic-Auth
----------------------------

One way to solve this problem, was to let the user give an
Authorization header when asking for a new token.

And make sure the same token would be generated for the same header.

This works really well, because you can then use a login:password and
always grab the same Hawk-Credentials for it.

In a nutshell it looks like this:

.. code-block:: python

    http POST localhost:8000/v1/tokens --auth admin:password -v
    
    POST /v1/tokens HTTP/1.1
    Accept: */*
    Accept-Encoding: gzip, deflate, compress
    Authorization: Basic YWRtaW46cGFzc3dvcmQ=
    Content-Length: 0
    Host: localhost:8000
    User-Agent: HTTPie/0.8.0
    
    HTTP/1.1 201 Created
    Content-Length: 266
    Content-Type: application/json; charset=UTF-8
    Date: Fri, 07 Nov 2014 15:09:01 GMT
    Server: waitress
    
    {
        "credentials": {
            "algorithm": "sha256",
            "id": "371ef18f8a054e5c9fb0961cc5b81006080e9ad22078d30b3727c7c32843579f",
            "key": "87e72a8e5dcaf8b4be00b8729462814da3d438ce2fd8b6efee335db722d8369d"
        },
        "token": "9f19de0237c9bd59f803de1785f7aea4e3499b6929df3428e1b415fed81f797a"
    }


Get a token from Firefox Account using OAuth
--------------------------------------------

Basic-Auth is good but it means you need to enter your login password
in the client app and trust the usage they will do with it.

Also for some application you want to trust the email address of the
user.

One way to do that is to use Firefox Account. The email used has been
validated and the login is made on a trusted Mozilla server.

The OAuth flow works as defined here:

1. You access you service ``http://service/oauth/params`` url to get the OAuth configuration in ``conf``
2. The app redirect the user to::

    GET conf.oauth_uri + "/authorization?" +
      "client_id=" + conf.client_id +
      "&state=" + conf.state +
      "&scope=profile&action=signin"

3. The user logs in in the OAuth identity provider
4. After the password has been validated, the OAuth IDP redirect the user to ``http://service//oauth/token?state=<state>&code=<code>``
5. Then the server ask ``POST conf.oauth_uri + "/token"`` with the ``code``, ``client_id`` and ``client_secret`` to get an ``access_token``.
6. The ``access_token`` can then be used to ask about the user profile: ``GET conf.profile_uri + "/profile"`` with ``Authorization: Bearer <access_token>`` header.
7. From the profile you can get the ``email``, ``avatar`` and ``uid`` of the user.


You have got an example of the view implementations here: https://github.com/spiral-project/daybed-fxa-oauth

Other authentication backends
-----------------------------

We have made this Authentication layer a pluggable layer so that you
can deploy Daybed with any of the one you'd like as well as all of
them.

You have another example for the BrowserID protocol here: https://github.com/spiral-project/daybed-browserid 

You can use it with Persona, Firefox Account BrowserId and even MSISDN-Gateway to let people log using their phone number.

This plugins can also help you to implement other authentication backends for Daybed. (SAML, other OAuth)
