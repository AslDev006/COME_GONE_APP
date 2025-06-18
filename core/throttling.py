from rest_framework.throttling import SimpleRateThrottle


class UserFieldRateThrottle(SimpleRateThrottle):
    scope = 'user_field_post'

    def get_cache_key(self, request, view):
        if request.method == 'POST' and request.data and 'user' in request.data:
            try:
                user_ident = str(request.data.get('user'))
                if user_ident:
                    return self.cache_format % {
                        'scope': self.scope,
                        'ident': user_ident
                    }
            except (KeyError, ValueError, TypeError):
                pass

        return None