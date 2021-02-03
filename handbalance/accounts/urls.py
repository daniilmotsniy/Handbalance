from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_page),
    path('register', views.register_page),
    path('logout', views.logout_user),
    path('account', views.account_page),
    path('diary', views.diary_page),
    path('leaders', views.leaders),
    path('completeTask/<int:task_id>', views.complete_task),
    path('completeBlock/<int:block_id>', views.complete_block),
    path('returnTask/<int:task_id>', views.return_task),
    path('returnAllTasks', views.return_all_tasks)
]
