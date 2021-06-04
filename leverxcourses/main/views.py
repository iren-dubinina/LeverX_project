from django.contrib.auth import get_user_model
from django.db import DatabaseError
from django.http import Http404
from rest_framework import generics, mixins, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, AllowAny
from rest_framework.response import Response

from . import serializers
from .models import Course, Lecture, LectureTask, TaskControl, TaskComments
from .permissions import LecturerOrGetPermissions
import logging

logger = logging.getLogger('django')


#################################COURSES#################################
class CourseList(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    """
    API endpoint that allows get list of user's current courses
    and create new courses
    """
    serializer_class = serializers.CourseSerializer
    permission_classes = [LecturerOrGetPermissions]

    def get_queryset(self):
        return Course.objects.filter(users=self.request.user)

    def get(self, request, *args, **kwargs):
        logger.info('Get Courses List for user')
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logger.info('Add new Course for user')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_course = serializer.save()
        new_course.users.add(self.request.user)
        headers = self.get_success_headers(serializer.data)
        result = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return result


class CourseDetail(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    """
    API endpoint that allows update and delete courses
    """
    serializer_class = serializers.CourseSerializer
    permission_classes = [LecturerOrGetPermissions]

    def get_queryset(self):
        return Course.objects.filter(users=self.request.user)

    def get(self, request, *args, **kwargs):
        logger.info('Get Course')
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        logger.info('Update Course')
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        logger.info('Delete Course')
        return self.destroy(request, *args, **kwargs)


#################################LECTURES#################################
class LectureList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    API endpoint that allows get list of user's current lectures
    and create new lectures
    """
    serializer_class = serializers.LectureSerializer
    permission_classes = [LecturerOrGetPermissions]

    def get_queryset(self):
        return Lecture.objects.filter(course__users=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LectureDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    serializer_class = serializers.LectureSerializer
    permission_classes = [LecturerOrGetPermissions]
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        return Lecture.objects.filter(course__users=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


#################################TASKS#################################

class TaskList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
    API endpoint that allows get list of user's current tasks
    and create new tasks
    """
    serializer_class = serializers.TaskSerializer
    permission_classes = [LecturerOrGetPermissions]

    def get_queryset(self):
        return LectureTask.objects.filter(lecture__course__users=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TaskDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """
    API endpoint that allows get, update, delete tasks
    """
    serializer_class = serializers.TaskSerializer
    permission_classes = [LecturerOrGetPermissions]

    def get_queryset(self):
        return LectureTask.objects.filter(lecture__course__users=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


##############################TaskControl#################################
class TaskControlList(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):
    """
    API endpoint that allows get list of user's current home tasks
    and create new home tasks
    """
    serializer_class = serializers.TaskControlSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return TaskControl.objects.filter(task__lecture__course__users=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TaskControlDetail(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    """
    API endpoint that allows get, update, delete home tasks
    """
    serializer_class = serializers.TaskSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return TaskControl.objects.filter(task__lecture__course__users=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


##############################TaskComments#################################
class TaskCommentsList(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    """
    API endpoint that allows get list of user's comments in home tasks
    and create new comments
    """
    serializer_class = serializers.TaskControlSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return TaskComments.objects.filter(taskcontrol__task__lecture__course__users=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TaskCommentsDetail(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    """
    API endpoint that allows get, update, delete comments in home tasks
    """
    serializer_class = serializers.TaskSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return TaskComments.objects.filter(task__lecture__course__users=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
