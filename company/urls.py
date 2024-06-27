from django.urls import path
from . import views

app_name = "company"

urlpatterns = [
    # # ====== Company Urls ======
    path("list/", views.CompanyList.as_view(), name="list"),
    path("<str:uuid>/profile/", views.CompanyProfile.as_view(), name="profile"),
    path("dashboard/", views.CompanyDashboard.as_view(), name="dashboard"), # Access only for company admin
    # ====== Center Urls ======
    path("center/list/", views.CenterList.as_view(), name="center-list"),
    path("center/<str:uuid>/profile/", views.CenterProfile.as_view(), name="center-profile"),
    path("accelerator/dashboard/", views.AcceleratorDashboard.as_view(), name="acc-dashboard"),
    path("accelerator/new-road/", views.CreateRoad.as_view(), name="new-road"),
    path("accelerator/<str:uuid>/update-road/", views.UpdateRoad.as_view(), name="update-road"),
    path("accelerator/<str:uuid>/delete-road/", views.DeleteRoad.as_view(), name="delete-road"),
    path("accelerator/save-collection-order/<str:road_uuid>/", views.save_collection_order, name="save-collection-order"),
    path("accelerator/delete-collection-order/<int:pk>/", views.delete_collection_order, name="delete-collection-order"),
    path("accelerator/new-collection/", views.CreateCollection.as_view(), name="new-collection"),
    path("accelerator/<str:uuid>/update-collection/", views.UpdateCollection.as_view(), name="update-collection"),
    path("accelerator/<str:uuid>/delete-collection/", views.DeleteCollection.as_view(), name="delete-collection"),
    path("accelerator/save-content-order/<str:collection_uuid>/", views.save_content_order, name="save-content-order"),
    path("accelerator/delete-content-order/<int:pk>/", views.delete_content_order, name="delete-content-order"),
    path("accelerator/new-content/", views.CreateContent.as_view(), name="new-content"),
    path("accelerator/<str:uuid>/update-content/", views.UpdateContent.as_view(), name="update-content"),
    path("accelerator/<str:uuid>/delete-content/", views.DeleteContent.as_view(), name="delete-content"),
    path("accelerator/new-exam/", views.CreateExam.as_view(), name="new-exam"),
    path("accelerator/<str:uuid>/update-exam/", views.UpdateExam.as_view(), name="update-exam"),
    path("accelerator/<str:uuid>/delete-exam/", views.DeleteExam.as_view(), name="delete-exam"),
    path("accelerator/new-question/<str:exam_uuid>/", views.new_question, name="new-question"),
    path("accelerator/<int:pk>/update-question/", views.UpdateQuestion.as_view(), name="update-question"),
    path("accelerator/delete-question/<int:pk>/", views.delete_question, name="delete-question"),
    path("accelerator/new-answer/<int:question_id>/", views.new_answer, name="new-answer"),
    path("accelerator/delete-answer/<int:pk>/", views.delete_answer, name="delete-answer"),
    path("accelerator/save-exam-order/<str:collection_uuid>/", views.save_exam_order, name="save-exam-order"),
    path("accelerator/delete-exam-order/<int:pk>/", views.delete_exam_order, name="delete-exam-order"),
    path("accelerator/new-task/", views.new_task, name="new-task"),
    path("accelerator/<str:uuid>/update-task/", views.UpdateTask.as_view(), name="update-task"),
    path("accelerator/<str:uuid>/delete-task/", views.DeleteTask.as_view(), name="delete-task"),
    path("accelerator/save-task-order/<str:collection_uuid>/", views.save_task_order, name="save-task-order"),
    path("accelerator/delete-task-order/<int:pk>/", views.delete_task_order, name="delete-task-order"),
    path("new-subject/", views.NewSubject.as_view(), name="new-subject"),
    path("team-management/", views.TeamManagement.as_view(), name="team-management"),
    path("all-requests/", views.AllRequests.as_view(), name="all-requests"),
    path("invest-management/", views.InvestManagement.as_view(), name="invest-management"),
    path("accelerator/new-register-task/", views.CreatePreRegisterTask.as_view(), name="new-register-task"),
    path("accelerator/<str:uuid>/update-register-task/", views.UpdatePreRegisterTask.as_view(), name="update-register-task"),
    path("accelerator/save_pre_register_task_question/<str:pre_register_task_uuid>/", views.save_pre_register_task_question, name="save_pre_register_task_question"),
    path("accelerator/delete_pre_register_task_question/<str:uuid>/", views.delete_pre_register_task_question, name="delete_pre_register_task_question"),

    path("accelerator/<str:uuid>/delete-register-task/", views.DeletePreRegisterTask.as_view(), name="delete-register-task"),
    path("accelerator/referee-management/", views.RefereeManagement.as_view(), name="referee-management"),

    path('logoutt/', views.create_center, name='create_center'),
]
