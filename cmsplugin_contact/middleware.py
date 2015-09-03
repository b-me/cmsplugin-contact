from .models import Contact


class ForceResponseMiddleware:

    def process_response(self, request, response):
        if getattr(request, 'django_cms_contact_redirect_to', None):
            return request.django_cms_contact_redirect_to
        return response


class RewriteMethodForContactFormPOSTRequestMiddleware:
    """
    Middleware rewrites request method and stores information for render
    method of plugin to fix bug with contact form on page with other forms
    or formsets
    """

    def process_request(self, request):
        if request.method == 'POST' and 'my_name' in request.POST \
                and Contact.objects.filter(form_name=request.POST['my_name']) \
                .exists():
            request.method = 'GET'
            request.CMSPLUGIN_CONTACT = request.POST['my_name']
