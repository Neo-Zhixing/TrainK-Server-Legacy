from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.exceptions import NotAcceptable


class VersatileViewMixin:
    def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)
            if not hasattr(request, 'accepted_renderer') or isinstance(request.accepted_renderer, TemplateHTMLRenderer):
                if hasattr(self, 'template_view'):
                    handler = self.template_view
                elif hasattr(self, 'template_views'):
                    handler = self.template_views.get(self.action)
                else:
                    handler = None
                if not handler:
                    raise NotAcceptable()
                response = handler(request._request, *args, **kwargs)
            else:
                # Get the appropriate handler method
                if request.method.lower() in self.http_method_names:
                    handler = getattr(self, request.method.lower(),
                                      self.http_method_not_allowed)
                else:
                    handler = self.http_method_not_allowed

                response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


class MethodPermissionMixin:
    method_permission_classes = {}

    def get_permissions(self):
        permissions = self.method_permission_classes[self.request.method] \
            if self.request.method in self.method_permission_classes \
            else self.permission_classes
        return [permission() for permission in permissions]
