from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_swagger.views import get_swagger_view

from .views import home, send_json

schema_view = get_schema_view(
    openapi.Info(
        title="Zipcho Development",
        default_version="v2",
        description="Zipcho Development Apis",
        contact=openapi.Contact(email="zipcho@zipcho.com"),
        license=openapi.License(name="development")  
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', home, name='home'),
    path('authentication/', include('authentication.urls')),
    # path('portfolio/', include('post.urls')),
    #path('notification/', include('notificationService.urls')),
    #path('search/', include('searchService.urls')),
    path('zipchoAdmin/', include('zipchoAdmin.urls')),
    
    # Spectacular 
    path("schema/", SpectacularAPIView.as_view(), name= "schema"),
    re_path(r'^zipchoSchema.json', send_json, name = 'send-json'),
    #path('zipchoSchema/', send_json, name = 'send-json'),

    path("swagger/",
        SpectacularSwaggerView.as_view(
            template_name="swagger-ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),

    #re_path(r'^swagger(?P<format>\.json)', 
    #        SpectacularSwaggerView.as_view(template_name="schema.json"),
    #        name='schema-json'),

    #path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"),
    #    name="swagger-ui"),
    path("swagger/redoc/", SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'),

    #path('swagger/', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    
    #re_path(r'^swagger(?P<format>\.json)$',
    #        schema_view.without_ui(cache_timeout=0),
    #        name='schema-json'),

    #path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]



