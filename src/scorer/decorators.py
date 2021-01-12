import inspect
import traceback
from functools import wraps


def ErrorDefender(func):

    @wraps(func)
    def wrapper(*a, **kw):
        class_method = str(func)
        try:
            return func(*a, **kw)
        except NotImplementedError as e:
            raise e
        except BaseException as e:
            error = str(e)
            print(f"An error occurred in {class_method}: {error}")
            print(traceback.format_exc())
            return {
                'class_method': class_method,
                'error': error,
                'class_error': e.__class__.__name__
            }
    return wrapper


def decorate_all_methods(decorator, exclude=None):
    if exclude is None:
        exclude = ['__init__']

    def apply_decorator(cls):
        for k, f in cls.__dict__.items():
            if inspect.isfunction(f) and k not in exclude:
                setattr(cls, k, decorator(f))
        return cls
    return apply_decorator
