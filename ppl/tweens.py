from raven import Client
from pyramid.renderers import render_to_response
def exception_tween_factory(handler, registry):
    settings = registry.settings
    if not settings.get('sentry.enabled', None):
        return handler
    dsn = settings.get('sentry.host', None)
    if not dsn:
        return handler
    client = Client(dsn)

    def sentry_tween(request):
        try:
            response = handler(request)
        except Exception:
            client.captureException()
            return render_to_response('500.html', {}, request)
        else:
            return response

    return sentry_tween
