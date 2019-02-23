from django.urls import path
from . import views

app_name = 'axf'

urlpatterns = [
    path('home/', views.home, name="home"),
    path('market/<int:categoryid>/<int:cid>/<int:sortid>/', views.market, name="market"),
    path('cart/', views.cart, name="cart"),
    path('mine/', views.mine, name="mine"),
    path('login/',views.login,name="login"),
    path('register/',views.register,name = "register"),
    path('checkuserid/',views.checkuserid,name = "checkuserid"),
    path('quit/',views.quit,name = "quit"),
    path('changecart/<int:type>/',views.changecart,name = "changecart"),
    path('consignee/',views.consignee,name = "consignee"),
    path('alladdr/',views.alladdr,name = "alladdr"),
    path('deladdr/',views.deladdr,name = "deladdr"),
    path('addrchose/',views.addrchose,name = "addrchose"),
    path('order/<int:type>/',views.order,name = "order"),
    path('getorder/',views.getorder,name = "getorder"),
    path('delorder/',views.delorder,name = "delorder"),
    path('status/<int:type>/',views.status,name = "status"),
    path('comment/',views.comment,name = "comment"),
    path('savecomm/',views.savecomm,name = "savecomm"),
    path('goodsinfo/<int:goodsid>/',views.goodsinfo,name = "goodsinfo"),
    path('', views.home),
]
