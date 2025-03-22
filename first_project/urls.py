from django.urls import path
from hello import views

urlpatterns = [
    # Страница с диаграммой
    path("", views.index, name="home"),

    # Страницы для реддактирования БД 
    path("edit/", views.edit_expenses, name="edit_expenses"),
    path("delete/<int:expense_id>/", views.delete_expense, name="delete_expense"),
]
