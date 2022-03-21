from tortoise import Model, fields


class Division(Model):
    name = fields.CharField(max_length=16, unique=True)
    description = fields.CharField(max_length=100, default='')
    pinned = fields.JSONField(default=list, description='置顶帖')

    def __str__(self):
        return self.name


class Tag(Model):
    name = fields.CharField(max_length=16, unique=True)
    temperature = fields.IntField(db_index=True, default=0)  # 该标签下的主题帖数

    def __str__(self):
        return self.name


class Hole(Model):
    time_created = fields.DatetimeField(auto_now_add=True)
    time_updated = fields.DatetimeField(auto_now=True, db_index=True)
    tags = fields.ManyToManyField('models.Tag', null=True)
    division = fields.ForeignKeyField('models.Division', on_delete=fields.CASCADE)
    view = fields.IntField(db_index=True, default=0)  # 浏览量
    reply = fields.IntField(db_index=True, default=-1)  # 如果只有首条帖子的话认为回复数为零
    mapping = fields.JSONField(default=dict)  # {user.id: anonymous_name}
    hidden = fields.BooleanField(default=False)  # 帖子是否隐藏

    def __str__(self):
        return f'树洞#{self.pk}'


class Floor(Model):
    hole = fields.ForeignKeyField('models.Hole', on_delete=fields.CASCADE)
    content = fields.TextField()
    anonyname = fields.CharField(max_length=16)
    user = fields.ForeignKeyField('models.User', fields.CASCADE)
    mention = fields.ManyToManyField('models.Floor', null=True, symmetrical=False, related_name='mentioned_by')
    time_created = fields.DatetimeField(auto_now_add=True)
    time_updated = fields.DatetimeField(auto_now=True)
    like = fields.IntField(default=0, db_index=True)  # 赞同数
    like_data = fields.JSONField(default=list)  # 点赞记录，主键列表
    deleted = fields.BooleanField(default=False)  # 仅作为前端是否显示删除按钮的依据
    fold = fields.JSONField(default=list)  # 折叠原因，字符串列表（原因由前端提供）
    special_tag = fields.CharField(max_length=16, default='')  # 额外字段
    storey = fields.IntField(default=0)  # 楼层数

    def __str__(self):
        return f"{self.content[:50]}"


class FloorHistory(Model):
    content = fields.TextField()
    altered_by = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE)
    altered_time = fields.DatetimeField(auto_now_add=True)
