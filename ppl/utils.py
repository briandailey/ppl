import re
import hashlib
from unicodedata import normalize

from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.orm.exc import NoResultFound

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))

def gravatar(email, size=100, rating='g', default='retro', force_default=False,
             force_lower=False, use_ssl=False):
    if email is None:
        email = ''
    if use_ssl:
        url = "https://secure.gravatar.com/avatar/"
    else:
        url = "http://www.gravatar.com/avatar/"
    if force_lower:
        email = email.lower()
    hashemail = hashlib.md5(email).hexdigest()
    link = "{url}{hashemail}?s={size}&d={default}&r={rating}".format(
        url=url, hashemail=hashemail, size=size,
        default=default, rating=rating)
    if force_default:
        link = link + "&f=y"
    return link

def get_object_or_404(Klass, **kwargs):
    try:
        obj = Klass.query.filter_by(**kwargs).one()
    except NoResultFound:
        raise HTTPNotFound('Group not found')

    return obj
