# throttles.py
from rest_framework.throttling import UserRateThrottle


class UserFieldRateThrottle(UserRateThrottle):
    scope = 'user_field_post'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        user_id_from_data = request.data.get('user')
        if user_id_from_data:
            return f'throttle_{self.scope}_{ident}_{user_id_from_data}'

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }