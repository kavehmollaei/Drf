from rest_framework import serializers
from .models import WireGuardServer, WireGuardClient
from .utils import *
class WireGuardServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WireGuardServer
        fields = '__all__'
        read_only_fields = ('private_key', 'public_key', 'created_at', 'updated_at')
        

class WireGuardServerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WireGuardServer
        fields = [
            'id', 'name', 'interface_name', 'address_cidr',
            'listen_port', 'public_endpoint', 'dns', 'allowed_ips'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        private_key = generate_private_key()
        public_key = generate_public_key(private_key)

        return WireGuardServer.objects.create(
            private_key=private_key,
            public_key=public_key,
            **validated_data
        )
class WireGuardClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = WireGuardClient
        fields = '__all__'
        read_only_fields = (
            'private_key', 'public_key', 'preshared_key',
            'address', 'created_at'
        )
class WireGuardClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WireGuardClient
        fields = ['id', 'name', 'dns', 'description']
        read_only_fields = ['id']

    def create(self, validated_data):
        server = self.context['server']
        private_key = generate_private_key()
        public_key = generate_public_key(private_key)
        preshared_key = generate_preshared_key()
        address = get_next_client_ip(server)

        return WireGuardClient.objects.create(
            server=server,
            private_key=private_key,
            public_key=public_key,
            preshared_key=preshared_key,
            address=address,
            **validated_data
        )