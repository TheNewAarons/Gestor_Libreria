from rest_framework import permissions

class IsJefeDeBodega(permissions.BasePermission):
    """
    Permite acceso solo a usuarios con rol 'Jefe de Bodega'.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.rol == 'Jefe de Bodega')
