"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
# from channels.auth import AuthMiddlewareStack
# from channels.routing import URLRouter
# from channels.routing import ProtocolTypeRouter
# from channels.security.websocket import AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application
# import RideSharing.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
application = get_asgi_application()


# application = ProtocolTypeRouter(
#     {
#     "http": django_asgi_app,
#     "websocket": AllowedHostsOriginValidator(
#     AuthMiddlewareStack(URLRouter(RideSharing.routing.websocket_urlpatterns))
#     )
#     }
# )
