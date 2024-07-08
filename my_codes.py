from datetime import datetime, timezone
from pydantic import field_validator, TypeAdapter, BaseModel
from typing import Optional
from typing_extensions import NotRequired, TypedDict

class IdentityCard(TypedDict):
    name: str
    surname: str
    identity_number: str
    birth_date: datetime
    valid_until: NotRequired[datetime]

    @field_validator('valid_until', mode='wrap')
    def valid_until_check(cls, input_value, _):
        if input_value == None:
            return datetime.now()
        return input_value
    
    @field_validator('identity_number', mode='wrap')
    def identity_check(cls, input_value, _):
        if input_value.startswith('0'):
            raise TypeError(f'{input_value} Invalid identity')
        return input_value
    
params = {'name': 'Yusuf',
          'surname': 'Çakır',
          'identity_number': '1234567890',
          'birth_date': '2020-01-01T12:00',
          'valid_until': None}

params_with_error = {'name': 'Yusuf',
          'surname': 'Çakır',
          'identity_number': '0234567890',
          'birth_date': '2002-01-01T12:00',
          'valid_until': '2024-01-01T12:00'}

adapter = TypeAdapter(IdentityCard)
result = adapter.validate_python(params)
print(result)
#{'name': 'Yusuf', 'surname': 'Çakır', 'identity_number': '1234567890', 'birth_date': datetime.datetime(2020, 1, 1, 12, 0), 'valid_until': datetime.datetime(2024, 7, 8, 15, 12, 57, 126757)}

try:
    result2 = adapter.validate_python(params_with_error)
except TypeError as e:
    print(e)
    # 0234567890 Invalid identity

print("#" * 50)

class Card(BaseModel):
    card_number: int
    firstname: str
    lastname: str
    valid_until: Optional[datetime] = "2030-01-01"

customer = Card(card_number=123455667890, firstname='Yusuf', lastname='Çakır')
print(customer)
