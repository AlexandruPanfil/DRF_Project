from rest_framework import routers

from PC.views import ViewSetPCAPIView

# Difference between DefaultRouter and SimpleRouter is in linking to pages (in debug mode)


# Do not do my mistake, write () in the end of ...Router()
# If we define this router we will use ViewSet at maximum, in a single page
# you will have all http requests (get, post, put, delete)
router = routers.DefaultRouter()

# Here we need to define the r'{route}' and our ViewSet,
# if you do not use queryset(model) in ViewSet, then you will have to define basename (the name of model)
router.register(prefix=r"router", viewset=ViewSetPCAPIView,)

# print(router.urls)


# This is a simple exemple of Router (get from documentation)
class MyCustomRouter(routers.SimpleRouter):
    routers = [
        routers.Route(url=r'{prefix}',
                      mapping={'get': 'list'},
                      name='{basename}--list',
                      detail=False,
                      initkwargs={'suffix': 'List'},),
        routers.Route(url=r'{prefix}',
                      mapping={'get': 'retrieve'},
                      name='{basename}--detail',
                      detail=True,
                      initkwargs={'suffix': 'Detail'}),
    ]