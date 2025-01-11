"""
Use check_email_leaks('email') to check data leaks.
- If invalid email syntax, raise ValueError.
- If email has no found leaks, return [].
- If email has leaks, return a list of (site_name='Site', date='Date') tuples.
"""

import typing
import re
from leakcheck import LeakCheckAPI_Public

Source = typing.NamedTuple("Source", [('site_name', str), ('date', str)])

def is_valid_email(email) -> bool:
    """Checks if the input email has a valid format (name@provider.tld)"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # define regex pattern
    return re.match(pattern, email) is not None  # match email against pattern

def check_email_leaks(email: str):
    if not is_valid_email(email):
        raise ValueError()  # if email inputted is not valid format, raise ValueError
    public_api = LeakCheckAPI_Public()  # initialize without an API key
    # TRY EXCEPT TO CHECK IF ANY LEAKS. IF NONE, RETURN []. ELSE, RETURN LIST OF LEAKS.
    try:
        api_data = public_api.lookup(query=email)  # perform a public lookup
    except:
        return []
    return output_leaks(api_data)  # if leaks exist, return list of leaks

def output_leaks(data):
    """Returns a list with [Leak Company, Date] pairs."""
    output = []
    for i in range (len(data['sources'])):
        output.append(Source(site_name=data['sources'][i]['name'], date=data['sources'][i]['date']))
    return output
