from sanic import Sanic
from tortoise import Model, fields

app = Sanic.get_app()


class User(Model):
    @staticmethod
    def _default_config():
        """
        show_folded: 对折叠内容的处理
            fold: 折叠
            hide: 隐藏
            show: 展示
        """
        return {
            'show_folded': 'fold'
        }

    nickname = fields.CharField(max_length=16, default='')
    favorites = fields.ManyToManyField('models.Hole', related_name='favored_by', null=True)
    # silenced = fields.JSONField(default=dict)
    config = fields.JSONField(default=_default_config)
    is_admin = False

    # 权限在auth服务中统一配置
    # def is_silenced(self, division_id):
    #     now = datetime.now(app.config['TZ'])
    #     division = str(division_id)  # JSON 序列化会将字典的 int 索引转换成 str
    #     if not self.silenced.get(division):  # 未设置禁言，返回 False
    #         return False
    #     else:
    #         expire_time = parser.isoparse(self.silenced.get(division))
    #         return expire_time > now

    def __str__(self):
        return f"用户#{self.pk}"
