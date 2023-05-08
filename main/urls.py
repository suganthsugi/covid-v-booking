from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.listcentres, name="listcentre"),
    path('success', views.success, name="success"),
    path('addcentre/', views.addcentre, name="addcentre"),
    path('updatecentre/<int:pk>/', views.updatecentre, name='updatecentre'),
    path('removecentre/<int:pk>/', views.removecentre, name='removecentre'),
    path('adddosage/<int:pk>/', views.adddosage, name='adddosage'),
    path('dosagelist/<int:pk>', views.dosagelist,name='dosagelist'),
    path('bookslot/', views.bookslot, name='bookslot'),
    path('adminlistcentre/', views.adminlistcentres, name='adminlistcentre'),
    path('slotcreate/<int:pk>/', views.create_slot, name='slotcreate'),
    path('slotupdate/<int:pk>/', views.slot_update, name='slotupdate'),
    path('slotdelete/<int:pk>/', views.slot_delete, name='slotdelete'),
    path('slotlist/<int:pk>/', views.slotlist, name='slotlist'),

   
]
