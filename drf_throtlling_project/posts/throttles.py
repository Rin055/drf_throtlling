from rest_framework.throttling import SimpleRateThrottle
from rest_framework.exceptions import Throttled

class PostCreateThrottle(SimpleRateThrottle):
    scope = 'post_create_custom'

    def allow_request(self, request, view):
        if request.method != "POST":
            return True
        return super().allow_request(request, view)

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.id
        else:
            ident = self.get_ident(request)

        return f'post-create-{ident}'

    def throttle_failure(self):
        raise Throttled(detail="Too many post creation requests. Please wait before creating another post.")
