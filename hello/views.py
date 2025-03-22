from django.shortcuts import render, redirect

#рисование диаграммы
import matplotlib
matplotlib.use('Agg')  # Отключаем Tkinter и включаем поддержку рендеринга без GUI
import matplotlib.pyplot as plt
import io
import base64

# База данных
from django.db import models
from .models import Expense  # Импортируем модель

#рисуем диаграмму
def draw_diag(categories, amounts):
    # Палитра цветов
    colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0", "#ffb3e6"]

    # Создаем стильную диаграмму
    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(
        amounts,
        labels=categories,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        wedgeprops={"edgecolor": "black", "linewidth": 1, "antialiased": True},
        textprops={'fontsize': 12, 'color': 'black'}
    )

    # Добавляем стиль тени для 3D-эффекта
    for w in wedges:
        w.set_edgecolor('black')
        w.set_linewidth(1.2)

    # Улучшаем подписи процентов
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_weight('bold')

    # Заголовок с улучшенным шрифтом
    plt.title('Расходы по категориям', fontsize=14, fontweight='bold', pad=20)

    # Сохраняем в буфер памяти и конвертируем в base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"


#создаем и сохраняем диаграмму
def generate_pie_chart():

    # Достаем данные из базы
    data = Expense.objects.values("category").annotate(total_amount=models.Sum("amount"))

    # Разбираем данные для построения графика
    categories = [item["category"] for item in data]
    amounts = [item["total_amount"] for item in data]

    # Возвращаем нарисованную диаграмму
    return draw_diag(categories, amounts)



#обрабатываем маршруты 
def index(request):
    chart = generate_pie_chart()
    return render(request, 'index.html', {'chart': chart})

# Страница редактирования расходов
def edit_expenses(request):
    if request.method == "POST":  # Проверяем, была ли отправлена форма
        category = request.POST.get("category")  # Получаем категорию из формы
        amount = request.POST.get("amount")  # Получаем сумму из формы

        if category and amount:  # Проверяем, что данные есть
            Expense.objects.create(category=category, amount=float(amount))  # Добавляем в БД

        return redirect("edit_expenses")  # Перенаправляем обратно на страницу

    expenses = Expense.objects.all()  # Загружаем все расходы из БД
    return render(request, "edit_expenses.html", {"expenses": expenses})  # Отображаем страницу

# Удаление расхода
def delete_expense(request, expense_id):
    Expense.objects.filter(id=expense_id).delete()  # Удаляем расход с нужным ID
    return redirect("edit_expenses")  # Перенаправляем обратно