from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_page),
    path('register', views.register_page),
    path('logout', views.logout_user),
    path('account', views.account_page),
    path('lesson/<int:block_id>', views.lesson),
    path('diary', views.diary_page),
    path('leaders', views.leaders),
    path('completeBlock/<int:block_id>', views.complete_block),
    path('returnBlock/<int:block_id>', views.return_block),
    path('returnAllTasks', views.return_all_tasks)
    # path('completeTask/<int:block_id>/<int:task_id>', views.complete_task),
    # path('returnTask/<int:block_id>/<int:task_id>', views.return_task),
]
