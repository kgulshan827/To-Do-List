from django.shortcuts import render
from .models import Task
from .serializers import TaskSerialzer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
# Create your views here.

class Tasklist(APIView):

    def get(self, request):
        Tasks = Task.objects.all()
        serializer = TaskSerialzer(Tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerialzer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class Taskdetail(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        Task = self.get_object(pk)
        serializer = TaskSerialzer(Task)
        return Response(serializer.data)

    def put(self, request, pk):
        Task = self.get_object(pk)
        serializer = TaskSerialzer(Task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Task = self.get_object(pk)
        Task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
