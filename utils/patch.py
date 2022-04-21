from fastapi import FastAPI


class MyFastAPI(FastAPI):
    app = None

    @classmethod
    def get_app(cls, **kwargs):
        if not cls.app:
            cls.app = MyFastAPI(**kwargs)
        return cls.app
