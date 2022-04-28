from tortoise import Model, fields


class User(Model):
    favorites = fields.ManyToManyField('models.Hole', related_name='favored_by', null=True)

    nickname: str
    config: dict
    is_admin: bool

    def __str__(self):
        return f"user#{self.pk}"


anonymous_user = User()
