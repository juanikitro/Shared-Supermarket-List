import functools
from .models import SimpleUser


def login_simulation_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.COOKIES.get("sessionid"):
            try:
                SimpleUser.objects.get(username=request.COOKIES.get("sessionid"))
                return view_func(request)
            except:
                raise BaseException("You must be logged in to perform this action")
        raise BaseException("You must be logged in to perform this action")

    return wrapper
