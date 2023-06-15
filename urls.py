from django.urls import path
from . import views

urlpatterns = [
    path('',views.welcomepage,name='welcomepagepath'),
    path('loginpage',views.loginpage,name='loginpagepath'),
    path('forgetpasswordpage',views.forgetpasswordpage,name='forgetpasswordpagepath'),
    path('active',views.active,name='activepath'),
    path('adminprofilepage',views.adminprofilepage,name='adminprofilepagepath'),
    path('deletestudent',views.deletestudent,name='deletestudentpath'),
    path('departmentassign/<int:n>/',views.departmentassign,name='departmentassignpath'),
    path('homepage',views.homepage,name='homepagepath'),
    path('inactive',views.inactive,name='inactivepath'),
    path('showstudent',views.showstudent,name='showstudentpath'),
    path('addstudent',views.addstudent,name='addstudentpath'),
    path('registerpage',views.registerpage,name='registerpagepath'),
    path('search',views.search,name='searchpath'),
    path('update2',views.update2,name='update2path'),
    path('signout',views.signout,name='signoutpath'),
    path('updateadmindata',views.updateadmindata,name='updateadmindatapath'),
    path('delstud/<int:z>/',views.delstud,name='delstudpath'),
    path('searchdown',views.searchdown,name='searchdownpath'),
    path('departmentassign/<int:n>/changedept',views.changedept,name='changedept'),
    path('studupdate',views.studupdate,name='studupdatepath')
]


