import pytest
from eminder.validation.inputvalidation import inputvalidation



# Testing the input validation
@pytest.mark.parametrize(
    "val_fields, expected", 
[
    ({"text":{"value":"Hej","type":"text","required":True}}, True),
    ({"text":{"value":"","type":"text","required":True}}, False),

    ({"email":{"value":"emil@emil.com","type":"email","required":True}}, True),
    ({"email":{"value":"Va","type":"email","required":True}}, False),

    ({"phone":{"value":"+46736487896","type":"phone","required":False}}, True),
    ({"phone":{"value":"123","type":"phone","required":False}}, False),

    ({"http":{"value":"https://www.google.com","type":"http","required":False}}, True),
    ({"http":{"value":"www.aftonbladet.com","type":"http","required":False}}, False),

    ({"interval":{"value":"15","type":"integer","required":False}}, True),
    ({"interval":{"value":"Invalid","type":"integer","required":False}}, False)

],
)
def test_inputvalidation(val_fields, expected):
    assert inputvalidation(val_fields) == expected

'''
Fields to input validate
val_fields = {
'scheduleinput':{'value':scheduleinput,'type':'integer','required':True},
'dateandtime':{'value':dateandtime,'type':'datetime','required':datetimereq},
'time':{'value':time,'type':'time','required':timereq},
'days':{'value':days,'type':'days','required':False},
'monthlydate':{'value':monthlydate,'type':'monthlydate','required':False},
'interval':{'value':interval,'type':'integer','required':False},
'channel':{'value':channel,'type':'integer','required':True},
'subject':{'value':subject,'type':'text','required':True},
'message':{'value':message,'type':'text','required':True}
}
'''