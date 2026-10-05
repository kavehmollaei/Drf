from django.db import models

# Create your models here.
class WireGuardServer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    interface_name = models.CharField(max_length=20, default='wg0')
    private_key = models.TextField()
    public_key = models.TextField()

    address_cidr = models.CharField(max_length=50)  # مثلا 10.10.0.1/24
    listen_port = models.PositiveIntegerField(default=51820)

    public_endpoint = models.CharField(max_length=255)  # مثلا vpn.example.com
    dns = models.CharField(max_length=255, blank=True, default='1.1.1.1')

    allowed_ips = models.CharField(max_length=255, default='10.10.0.0/24')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class WireGuardClient(models.Model):
    server = models.ForeignKey(WireGuardServer, related_name='clients', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    private_key = models.TextField()
    public_key = models.TextField()
    preshared_key = models.TextField(blank=True, default='')

    address = models.CharField(max_length=50)  # مثلا 10.10.0.2/32
    dns = models.CharField(max_length=255, blank=True, default='1.1.1.1')

    enabled = models.BooleanField(default=True)
    description = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('server', 'name')