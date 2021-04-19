from django.shortcuts import redirect


def unauthenticated_user(view_function):
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('residential:dashboard')
        else:
            return view_function(request, *args, **kwargs)

    return wrapper


def allowed_users(user_roles: list, redirect_link: str):
    def decorator(view_function):
        def wrapper(request, *args, **kwargs):

            group = None
            # check if user is assigned to a specific group
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            # if user meets the user role description -> allow page to be accessed
            if group in user_roles:
                return view_function(request, *args, **kwargs)
            else:
                return redirect(redirect_link)
        return wrapper
    return decorator