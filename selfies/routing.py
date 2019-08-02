from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import app.routing
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        try:
            token_key = scope["query_string"].decode().split("=")[1]
            if token_key:
                token = Token.objects.get(key=token_key)
                scope["user"] = token.user
                close_old_connections()
        except Token.DoesNotExist:
            scope["user"] = AnonymousUser()
        return self.inner(scope)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": TokenAuthMiddlewareStack(
            URLRouter(app.routing.websocket_urlpatterns)
        )
    }
)
