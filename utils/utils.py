from flask import session, request
from entities.VoteCard import VoteCard

def get_ip_address():
    
    try:
        ip_address = session['ip_addr']
    except KeyError:
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        session['ip_addr'] = ip_address
    return ip_address

def voting(obj: VoteCard, vote: str) -> None:
    
    if vote == 'upvote':
        obj.upvote()
    elif vote == 'downvote':
        obj.downvote()
    return None