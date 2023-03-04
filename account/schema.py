
from pydantic import BaseModel



class AccountByPhone(BaseModel):
    number: str

class CodeVerify(BaseModel):
    code: str


class AccountInfo(BaseModel):
    phonenumber: str = None
    auth_code: str = None
    # auth_expiration_date: Date = None
    sexe: str = None
    # about = fields.TextField( null = True)
    # relation = fields.CharField(max_length=60, null = True)
    # orientation = fields.ForeignKeyField('models.Orientation', related_name='orientation', null = True)
    # heigth = fields.FloatField(null=True)
    # hair = fields.CharField(max_length=60, null = True)
    # child = fields.CharField(max_length=60, null = True)
    # drink = fields.CharField(max_length=60, null = True)
    # smoking = fields.CharField(max_length=60, null = True)
    # country = fields.ForeignKeyField('models.Country', related_name='country', null = True)
    # birthday = fields.DateField(null = True)
    # ishidden = fields.BooleanField(default=False, null = True)
    # drink = fields.CharField(max_length=60, null = True)