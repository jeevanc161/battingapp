from django.views import  generic


class IndexPageView(generic.TemplateView):
    template_name = 'website/index.html'  # template name for view

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context.update({
            "abc": "ABC",
        })
        return context
