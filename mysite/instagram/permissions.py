from rest_framework import permissions


class CheckOwnerEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CheckUserProfileEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class CheckFollowEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.following == request.user or obj.follower == request.user
