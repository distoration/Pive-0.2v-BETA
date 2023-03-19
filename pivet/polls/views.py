from django.shortcuts import render
from rest_framework import generics
import rest_framework
from models import Task
from serializer import TaskSerializer

# Create your views here.
class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
