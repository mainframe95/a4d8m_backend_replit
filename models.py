from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class DateOfCreation(Model):
    id = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class User(DateOfCreation):
    username = fields.CharField(max_length=60, null=True)
    pwd = fields.CharField(max_length=255, null=True)
    salt = fields.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.id} {self.username}"


class Country(DateOfCreation):
    label = fields.CharField(max_length=60)
    code = fields.CharField(max_length=4)
    is_actived = fields.BooleanField(default=True)


class Orientation(DateOfCreation):
    label = fields.CharField(max_length=60)
    isActived = fields.BooleanField(default=True)


class Privacy(DateOfCreation):
    visibility = fields.BooleanField(default=True)
    share = fields.BooleanField(default=True)
    showLocation = fields.BooleanField(default=True)
    showGender = fields.BooleanField(default=True)


class Account(User):
    phonenumber = fields.CharField(max_length=20, null=True)
    auth_code = fields.CharField(max_length=5, null=True)
    auth_expiration_date = fields.DatetimeField(null=True)
    sexe = fields.CharField(max_length=60, null=True)
    about = fields.TextField(null=True)
    relation = fields.CharField(max_length=60, null=True)
    orientation = fields.ForeignKeyField(
        "models.Orientation", related_name="orientation", null=True
    )
    heigth = fields.FloatField(null=True)
    hair = fields.CharField(max_length=60, null=True)
    child = fields.CharField(max_length=60, null=True)
    drink = fields.CharField(max_length=60, null=True)
    smoking = fields.CharField(max_length=60, null=True)
    country = fields.ForeignKeyField(
        "models.Country", related_name="country", null=True
    )
    birthday = fields.DateField(null=True)
    ishidden = fields.BooleanField(default=False, null=True)
    drink = fields.CharField(max_length=60, null=True)


class Admin(User):
    firstname = fields.CharField(max_length=255)
    lastname = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    access = fields.CharField(max_length=255)



class Verified(DateOfCreation):
    account = fields.ForeignKeyField(
        model_name="models.Account", related_name="account"
    )
    Verified_by = fields.ForeignKeyField(
        model_name="models.Admin", related_name="admin"
    )
    proof = fields.CharField(max_length=255)
    is_actived = fields.BooleanField(default=False)

    def __str__(self):
        return f"{self.account} verified by {self.Verified_by} at {self.updated_at}"


class Banned(DateOfCreation):
    account = fields.ForeignKeyField(model_name="models.Account", related_name="ban")
    do_by = fields.ForeignKeyField(model_name="models.Admin", related_name="admin_do")
    motif = fields.TextField()

    def __str__(self) -> str:
        return f"{self.account} banned by {self.do_by} at {self.created_at} "


class Visite(DateOfCreation):
    viewer = fields.ForeignKeyField(model_name="models.Account", related_name="viewer")
    isSeen = fields.BooleanField(default=False)
    view_by = fields.ForeignKeyField(
        model_name="models.Account", related_name="view_by"
    )


class Orientation(DateOfCreation):
    label = fields.CharField(max_length=60)
    is_actived = fields.BooleanField(default=False)


class Genre(DateOfCreation):
    label = fields.CharField(max_length=60)
    is_actived = fields.BooleanField(default=False)


class Hobies(DateOfCreation):
    label = fields.CharField(max_length=255)
    is_actived = fields.BooleanField(default=True)


class HobiesTrans(DateOfCreation):
    label = fields.CharField(max_length=255)
    lang = fields.CharField(max_length=255)


class UserHobies(DateOfCreation):
    account = fields.ForeignKeyField(
        model_name="models.Account", related_name="account_hobies"
    )
    hobies = fields.ForeignKeyField(model_name="models.Hobies")
    is_actived = fields.BooleanField(default=True)


class Privacy(DateOfCreation):
    account = fields.ForeignKeyField(
        model_name="models.Account", related_name="account_privacy"
    )
    visibility = fields.BooleanField(default=True)
    share = fields.BooleanField(default=True)
    show_location = fields.BooleanField(default=True)
    show_gender = fields.BooleanField(default=True)

    def __str__(self):
        return f"{self.account} - {self.visibility}, {self.share}, {self.show_location} {self.show_gender}  "


class Country(DateOfCreation):
    name = fields.CharField(max_length=255)
    code = fields.CharField(max_length=3)
    is_actived = fields.BooleanField(default=False)


class ReportType(DateOfCreation):
    label = fields.CharField(max_length=255)
    is_actived = fields.BooleanField(default=False)


class Reports(DateOfCreation):
    concern = fields.ForeignKeyField(
        model_name="models.Account", related_name="concern_account"
    )
    report_type = fields.ForeignKeyField(
        model_name="models.ReportType", related_name="reports"
    )


class Like(DateOfCreation):
    id = fields.IntField(pk=True)
    initiate_by = fields.ForeignKeyField(
        model_name="models.Account", related_name="first"
    )
    relates_to = fields.ForeignKeyField(
        model_name="models.Account", related_name="second"
    )
    is_match = fields.BooleanField(default=False)
    isDeleted = fields.BooleanField(default=False)
    deleted_by = fields.ForeignKeyField(
        model_name="models.Account", related_name="deleted"
    )


class Favories(DateOfCreation):
    is_actived = fields.BooleanField(default=True)
    like = fields.ForeignKeyField(model_name="models.Like", related_name="Like")


class NotificationType(DateOfCreation):
    label = fields.CharField(max_length=255)
    is_actived = fields.BooleanField(default=False)


class NotificationParams(DateOfCreation):
    account = fields.ForeignKeyField(
        model_name="models.Account", related_name="account_param"
    )
    type = fields.ForeignKeyField(
        model_name="models.NotificationType", related_name="notification"
    )
    web = fields.BooleanField(default=False)
    app = fields.BooleanField(default=False)
    email = fields.BooleanField(default=True)


account_pydantic = pydantic_model_creator(Account, name="account")


# class Tournament(Model):
#     # Defining `id` field is optional, it will be defined automatically
#     # if you haven't done it yourself
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=255)

#     # Defining ``__str__`` is also optional, but gives you pretty
#     # represent of model in debugger and interpreter
#     def __str__(self):
#         return self.name


# class Event(Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=255)
#     # References to other models are defined in format
#     # "{app_name}.{model_name}" - where {app_name} is defined in tortoise config
#     tournament = fields.ForeignKeyField('models.Tournament', related_name='events')
#     participants = fields.ManyToManyField('models.Team', related_name='events', through='event_team')

#     def __str__(self):
#         return self.name


# class Team(Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=255)

#     def __str__(self):
#         return self.name
