# -*- coding: iso-8859-1 -*-
# This is some sample code you might find useful when you want to use some
# external cookie (made by some other program, not moin) with moin.
# See the XXX places for customizing it to your needs. You need to put this
# code into your farmconfig.py or wikiconfig.py.

# ...

class FarmConfig(DefaultConfig):
    def external_cookie(request):
        """ authenticate via external cookie """
        import Cookie
        cookiename = "whatever" # XXX external cookie name you want to use
        try:
            cookie = Cookie.SimpleCookie(request.saved_cookie)
        except Cookie.CookieError:
            # ignore invalid cookies
            cookie = None
        if cookie and cookie.has_key(cookiename):
            import urllib
            cookievalue = cookie[cookiename].value
            # XXX now we decode and parse the cookie value - edit this to fit your needs.
            # the minimum we need to get is auth_username. aliasname and email is optional.
            cookievalue = urllib.unquote(cookievalue) # cookie value is urlencoded, decode it
            cookievalue = cookievalue.decode('iso-8859-1') # decode cookie charset to unicode
            cookievalue = cookievalue.split('#') # cookie has format loginname#firstname#lastname#email
            
            auth_username = cookievalue[0] # having this cookie means user auth has already been done!
            aliasname = email = ''
            try:
                aliasname = "%s %s" % (cookievalue[1], cookievalue[2]) # aliasname is for cosmetical stuff only
                email = cookievalue[3]
            except IndexError: # XXX this is for debugging it, in case it does not work
                if 0:
                    f = open("cookie.log", "w")
                    f.write(repr(cookie))
                    f.write(repr(cookievalue))
                    f.close()
                pass

            from MoinMoin.user import User
            # giving auth_username to User constructor means that authentication has already been done.
            user = User(request, name=auth_username, auth_username=auth_username)
            
            changed = False
            if aliasname != user.aliasname: # was the aliasname externally updated?
                user.aliasname = aliasname ; changed = True # yes -> update user profile
            if email != user.email: # was the email addr externally updated?
                user.email = email ; changed = True # yes -> update user profile

            if not user.valid and not user.disabled or changed: # do we need to save/update?
                user.save() # yes, create/update user profile
            if user.valid: # did we succeed making up a valid user?
                return user # yes, return user object and stop processing auth method list
        return None # no, return None and continue with next method in auth list

    from MoinMoin.auth import moin_cookie, http
    # first try the external_cookie, then http basic auth, then the usual moin_cookie
    auth = [external_cookie, http, moin_cookie]

    # ... (rest of your config follows here) ...

