from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import EmailConfigForm
from .models import EmailConfig
from .serializers import ReviewSerializer
from .tasks import send_daily_review_summary


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class ReviewViews(APIView):

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def send_email_view(request):
    send_daily_review_summary()

    return HttpResponse('Email sent!')


def email_config_view(request):
    config = EmailConfig.objects.first()
    if request.method == 'POST':
        form = EmailConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            return redirect('email_config')
    else:
        form = EmailConfigForm(instance=config)
    return render(request, 'api/email_config.html', {'form': form})