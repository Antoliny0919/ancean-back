from rest_framework import permissions

class IsOwnerAndAdmin(permissions.BasePermission):
  
  def has_permission(self, request, view):
    self.message = '권한이 존재하지 않습니다.'
    
    # HTTP GET method only allow for common user
    if request.method in permissions.SAFE_METHODS:
      return True
    
    # verify that the requested user is an admin other than the HTTP GET method
    return bool(request.user and request.user.is_staff)
  
  def has_object_permission(self, request, view, obj):
    '''
    call via get_object only when requester and object to be fluctuated are associated
    '''
    self.message = '간단하게 객체와 요청자가 일치하지 않다는 에러'
    is_owner = request.user == obj.author
    
    return is_owner