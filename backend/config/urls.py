"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from api.blog.views import BlogViewSet
# DRFのviewsetを作成したなら、SimpleRouterにregisterします。
# 例えば、blogs/views.pyではBlogViewSethはviewsets.GenericViewSetを継承したクラスベースビューになっているが、これをurls.pyで登録するにはroute.registerするだけでいい。
# GenericAPIViewを継承したクラスベースビューだと、urlpattersにpathとして追加する 必要がでる。
router = routers.SimpleRouter()
router.register(r'api/v1/blogs', BlogViewSet, basename="blog")

# Djangoとしてはurlpatternsにrouterをincloudeしたpathを追加する
urlpatterns = [
    path('admin/', admin.site.urls),
    # ↓drg-spectacularによるドキュメント化のため↓2つを追加
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # viewsetを使えるようにするため追加
    path('', include(router.urls)),
    
]