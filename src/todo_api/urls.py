from django.urls import path, include
from .views import (TodoLisApiView,TodoDetailApiView, TodoViewSet, RetrieveDeleteItem, CreateListItems,
                    RetrieveUpdateDeleteItem, ListAPIItem, MovieCreateItem)
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api-viewset', TodoViewSet,)

urlpatterns = [
    path('api/', TodoLisApiView.as_view()),
    path('api/<int:todo_id>/', TodoDetailApiView.as_view()),
    path('', include(router.urls)),
    path('generic/<int:pk>/', RetrieveDeleteItem.as_view()),
    path('mixins/', CreateListItems.as_view()),
    path('mixins/<int:pk>/', RetrieveUpdateDeleteItem.as_view()),
    path('concreate-view/', ListAPIItem.as_view()),
    path('movie/create/', MovieCreateItem.as_view())
]