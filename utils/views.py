from rest_framework.settings import api_settings
from rest_framework.renderers import TemplateHTMLRenderer


def dispatch(apiView, templateView, **initkwargs):
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
	renderers = [renderer() for renderer in renderer_classes]

	content_negotiation_class = api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS
	conneg = content_negotiation_class()

	def view(request, *args, **kwargs):
		format_kwarg = kwargs.get(api_settings.FORMAT_SUFFIX_KWARG) if api_settings.FORMAT_SUFFIX_KWARG else None
		try:
			renderer, _ = conneg.select_renderer(request, renderers, format_kwarg)
		except Exception:
			renderer = renderers[0]

		handler = templateView if isinstance(renderer, TemplateHTMLRenderer) else apiView
		return handler(*args, **kwargs)
	return view
