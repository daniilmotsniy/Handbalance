from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_page),
    path('register', views.register_page),
    path('logout', views.logout_user),
    path('account', views.account_page),
    path('lesson1', views.lesson1),
    path('lesson2', views.lesson2),
    path('lesson3', views.lesson3),
    path('lesson4', views.lesson4),
    path('lesson5', views.lesson5),
    path('diary', views.diary_page),
    path('leaders', views.leaders),
    path('buy', views.buy),
    path('completeTask/<int:block_id>/<int:task_id>', views.complete_task),  # FIXME unused?
    path('completeBlock/<int:block_id>', views.complete_block),
    path('returnTask/<int:block_id>/<int:task_id>', views.return_task),  # FIXME unused?
    path('returnBlock/<int:block_id>', views.return_block),
    path('returnAllTasks', views.return_all_tasks)
]
