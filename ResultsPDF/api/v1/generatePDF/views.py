import os
import redis
import datetime
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .serializers import LinksListSerializer
from .tasks import send_links_pdf_email_task


r = redis.Redis(host=os.getenv('REDIS_SERVER'), port=6379, db=2, charset="utf-8", decode_responses=True)


class SuggestedLinksViewset(GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def data_sync(self, request):
        serializers = LinksListSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        data = serializers.validated_data
        time = datetime.datetime.now()
        r.zadd(request.user.id, {url: time.timestamp() for url in data})
        scheduled_run_time = time + datetime.timedelta(minutes=settings.PDF_LINK_EMAIL_BUFFER_TIME)
        send_links_pdf_email_task.apply_async(kwargs={'user_id': request.user.id,
                                                      'user_email': request.user.email,
                                                      'task_queue_push_time': time.timestamp()},
                                              eta=scheduled_run_time)
        return Response({'status': 1, 'message': 'data synced'})
