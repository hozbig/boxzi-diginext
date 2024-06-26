from django.urls import path
from . import views

app_name = "quiz"
urlpatterns = [
    path("<str:exam_uuid>-<str:collection_uuid>/exam/", views.ExamDetail.as_view(), name="exam-detail"),

    # ========= PreRegister Tasks and Tests:
    path("pre-register-required/<str:road_uuid>/", views.PreRegisterRequired.as_view(), name="pre-register-required"),
    path("pre-register-required-team/<str:road_uuid>/", views.PreRegisterRequiredTeam.as_view(), name="pre-register-required-team"),
    path("pre-register-required-individual/<str:road_uuid>/", views.PreRegisterRequiredIndividual.as_view(), name="pre-register-required-individual"),
    path("task-response-detail/<str:user_uuid>/", views.PreRegisterTaskResponseDetail.as_view(), name="task-response-detail"),

    path("iam-individual/<str:uuid>/", views.i_am_team_individual, name="iam-individual"),
    path("iam-tmember/<str:uuid>/", views.i_am_team_member, name="iam-tmember"),
    path("iam-coordinator/<str:uuid>/", views.i_am_team_coordinator, name="iam-coordinator"),

    path("personal-tests/<str:road_uuid>/", views.PreRegisterPersonalTests.as_view(), name="pre-register-personal-tests"),
    path("personal-tests-result/<str:user_uuid>/", views.PersonalTestsResult.as_view(), name="personal-tests-result"),
    path("pre-register-challenge/<str:road_uuid>/", views.PreRegisterChallenges.as_view(), name="pre-register-challenge"),
    path("save_task_question_response/<str:task_uuid>/<str:road_uuid>/", views.save_task_question_response, name="save_task_question_response"),
    path("pre-register-challenge-update/<str:task_res_uuid>/<str:road_uuid>/", views.PreRegisterChallengesUpdate.as_view(), name="pre-register-challenge-update"),
]