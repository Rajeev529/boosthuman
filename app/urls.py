from . import views
from . import llm
from django.urls import path

urlpatterns = [
    path("", views.homepage),
    path("product/<int:idx>/<slug:platform>/", views.product, name='product_page'),
    path("addwish", views.addwish),
    path("wishlist", views.wishlist, name="wishlist"),
    path("popuparr", views.popuparr),
    path("blog", views.blog),
    path("listing/<path:string>/", views.listing, name="listing"),
    path("listing2", views.listing2, name="listing2"),
    path("chatbot", llm.chatbot, name="chatbot"),
]