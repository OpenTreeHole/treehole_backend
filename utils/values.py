from datetime import datetime

from sanic import Sanic

app = Sanic.get_app()

LENGTH = 10


def now():
    return datetime.now(app.config['TZ'])


def default_config():
    """
    show_folded: 对折叠内容的处理
        fold: 折叠
        hide: 隐藏
        show: 展示
    """
    return {
        'show_folded': 'fold'
    }
