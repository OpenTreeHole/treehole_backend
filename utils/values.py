from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

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


class PageModel(BaseModel):
    offset: Optional[int] = 0
    size: Optional[int] = Field(
        default=config.default_size,
        le=config.max_size, ge=0
    )
    order: Optional[str] = '-id'

    class Config:
        # 好像没用
        allow_population_by_field_name = True
