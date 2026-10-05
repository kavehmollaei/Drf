from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import *
from django.http import FileResponse
from io import BytesIO
# Create your views here.

from rest_framework import generics
from .models import WireGuardServer, WireGuardClient
from .serializers import (
    WireGuardServerSerializer,
    WireGuardServerCreateSerializer,
    WireGuardClientSerializer,
    WireGuardClientCreateSerializer,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
class ServerListCreateView(generics.ListCreateAPIView):
    queryset = WireGuardServer.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WireGuardServerCreateSerializer
        return WireGuardServerSerializer


class ClientListCreateView(generics.ListCreateAPIView):
    serializer_class = WireGuardClientSerializer

    def get_queryset(self):
        server_id = self.kwargs['server_id']
        return WireGuardClient.objects.filter(server_id=server_id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WireGuardClientCreateSerializer
        return WireGuardClientSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['server'] = get_object_or_404(WireGuardServer, pk=self.kwargs['server_id'])
        return context

class ServerConfigView(APIView):
    def get(self, request, pk):
        server = get_object_or_404(WireGuardServer, pk=pk)
        return Response({
            "server_id": server.id,
            "name": server.name,
            "config": render_server_config(server)
        })
class ClientConfigView(APIView):
    def get(self, request, pk):
        client = get_object_or_404(WireGuardClient, pk=pk)
        return Response({
            "client_id": client.id,
            "name": client.name,
            "config": render_client_config(client)
        })
class ClientConfigDownloadView(APIView):
    def get(self, request, pk):
        client = get_object_or_404(WireGuardClient, pk=pk)
        config_text = render_client_config(client)

        buffer = BytesIO(config_text.encode('utf-8'))
        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f'{client.name}.conf',
            content_type='text/plain'
        )