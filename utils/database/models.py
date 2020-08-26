from tortoise.models import Model
from tortoise import fields


class User(Model):
    user_id = fields.BigIntField(unique=True)
    first_name = fields.TextField()
    last_name = fields.TextField(blank=True, null=True)
    username = fields.CharField(max_length=34, blank=True, null=True)
    phone_number = fields.BigIntField(null=True)
    lang = fields.CharField(max_length=2, null=True)

    def __str__(self):
        return f"{self.first_name} - {self.user_id}"
    
    class Meta:
        table = "users"


class Feedback(Model):
    id = fields.IntField(pk=True)
    text = fields.TextField()
    user = fields.ForeignKeyField('models.User')

    def __str__(self):
        return f"Feedback {self.id} - {self.user.first_name} {self.user.id}"
