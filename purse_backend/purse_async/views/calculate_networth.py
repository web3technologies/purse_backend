from rest_framework.views import APIView
from rest_framework.response import Response
from purse_async.tasks import calculate_networth_task



class CalculateNetworthView(APIView):

    def post(self, *args, **kwargs):
        task = calculate_networth_task.delay()
        return Response(data={"task": str(task)}, status=201)
