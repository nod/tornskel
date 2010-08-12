import re
import sys
import simplejson

# import code for encoding urls and generating md5 hashes for gravatar
import urllib, hashlib

from couchdbkit import Document, DocumentSchema, BadValueError, SchemaProperty
from couchdbkit.schema.properties import *
from couchdbkit.schema.properties_proxy import SchemaListProperty

# let's pull in our queue management functions
from os import path
sys.path.insert(0,path.join(path.dirname(__file__), "../../"))
import hcmailman.jobs

class RegexStringProperty(StringProperty):
    def __init__(self, pattern, **kwargs):
        StringProperty.__init__(self, **kwargs)
        self._pattern = re.compile(pattern)

    def validate(self, value, required=True):
        """
        Verifies that the string matches the pattern.  Note that it uses
        python's match() and not search().  If the first character of value
        does not match, the pattern does not match.
        """
        value = super(StringProperty, self).validate(value, required=required)
        if required and value and not self._pattern.match(value):
            raise BadValueError(
                '"%s" does not match "%s"'%(value,self._pattern.pattern)
                )
        return value


# generator pattern for class members
SlugProperty = lambda req=None: RegexStringProperty(r'^[\w-]+$', required=req)


class User(Document):
    email = StringProperty() # TODO: unique per user... -jk-
    password_hash = StringProperty()
    name = StringProperty()
    last_seen = DateTimeProperty(auto_now=True)
    created_at = DateTimeProperty(auto_now_add=True)
    auth_hash = StringProperty()
    confirmed = BooleanProperty()

    def __str__(self):
        return """<span class="user">%s</span>""" % (
            self.name if self.name else self.email
            )

    def to_d(self):
        return {'nm':self.name, 'e':self.email}


class Message(Document):
    user = SchemaProperty(User)
    from_user = SchemaProperty(User) # TODO: need a sys user? -jk-
    text = StringProperty()
    created_at = DateTimeProperty(auto_now_add=True)



