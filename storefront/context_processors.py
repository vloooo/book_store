from storefront.models import Genre, Author


def get_base_context(request):
    context = {'genres': Genre.objects.all(),
               'authors': Author.objects.all()}
    if request.user.is_active:
        context.update({'active_order': request.user.orders.filter(is_active=True).first()})
    return context

