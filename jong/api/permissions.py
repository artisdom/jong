from rest_framework import permissions


class DjangoModelPermissions(permissions.BasePermission):

    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['jong.add', 'jong.add'],
        'PUT': ['jong.change', 'jong.change'],
        'DELETE': ['jong.delete', 'jong.delete'],
    }
