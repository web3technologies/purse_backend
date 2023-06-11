from rest_framework import viewsets

from django_celery_results.models import TaskResult

from purse_async.serializers import TaskResultSerializer


class TaskResultViewset(viewsets.ModelViewSet):
    
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    lookup_field =  "task_id"

