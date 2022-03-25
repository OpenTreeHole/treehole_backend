from tortoise import Model, fields

from utils.values import default_config


class User(Model):
    nickname = fields.CharField(max_length=16, default='')
    favorites = fields.ManyToManyField('models.Hole', related_name='favored_by', null=True)
    config = fields.JSONField(default=default_config)
    is_admin = False

    def __str__(self):
        return f"用户#{self.pk}"
