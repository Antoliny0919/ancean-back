from rest_framework import permissions

class IsOwnerAndAdmin(permissions.BasePermission):
  
  def has_permission(self, request, view):
    
    # HTTP GET method only allow for common user
    if request.method in permissions.SAFE_METHODS:
      return True
    
    # verify that the requested user is an admin other than the HTTP GET method
    return bool(request.user and request.user.is_staff)
  
  def has_object_permission(self, request, view, obj):
    '''
    call via get_object only when requester and object to be fluctuated are associated
    '''
    is_owner = request.user == obj.author
    
    return is_owner