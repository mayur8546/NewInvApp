"""Permission set for InvenTree."""

from functools import wraps

from rest_framework import permissions

import users.models


class RolePermission(permissions.BasePermission):
    """Role mixin for API endpoints, allowing us to specify the user "role" which is required for certain operations.

    Each endpoint can have one or more of the following actions:
    - GET
    - POST
    - PUT
    - PATCH
    - DELETE

    Specify the required "role" using the role_required attribute.

    e.g.

    role_required = "part"

    The RoleMixin class will then determine if the user has the required permission
    to perform the specified action.

    For example, a DELETE action will be rejected unless the user has the "part.remove" permission
    """

    def has_permission(self, request, view):
        """Determine if the current user has the specified permissions."""
        user = request.user

        # Superuser can do it all
        if user.is_superuser:
            return True

        # Map the request method to a permission type
        rolemap = {
            'GET': 'view',
            'OPTIONS': 'view',
            'POST': 'add',
            'PUT': 'change',
            'PATCH': 'change',
            'DELETE': 'delete',
        }

        permission = rolemap[request.method]

        # The required role may be defined for the view class
        if role := getattr(view, 'role_required', None):
            return users.models.check_user_role(user, role, permission)

        try:
            # Extract the model name associated with this request
            model = view.serializer_class.Meta.model

            app_label = model._meta.app_label
            model_name = model._meta.model_name

            table = f"{app_label}_{model_name}"
        except AttributeError:
            # We will assume that if the serializer class does *not* have a Meta,
            # then we don't need a permission
            return True

        return users.models.RuleSet.check_table_permission(user, table, permission)


class IsSuperuser(permissions.IsAdminUser):
    """Allows access only to superuser users."""

    def has_permission(self, request, view):
        """Check if the user is a superuser."""
        return bool(request.user and request.user.is_superuser)


def auth_exempt(view_func):
    """Mark a view function as being exempt from auth requirements."""
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.auth_exempt = True
    return wraps(view_func)(wrapped_view)
