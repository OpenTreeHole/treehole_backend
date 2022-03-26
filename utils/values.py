from datetime import datetime

from config import config


def now():
    return datetime.now(config.tz)


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
