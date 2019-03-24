"""
all routes
"""

from controllers import *

routes = [
        (r'/login', Main.LoginHandler),
        (r'/logout', Main.LogoutHandler),
        ('/victiminfo', Victim.VictimInfo)
    ]
