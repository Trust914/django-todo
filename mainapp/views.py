from django.shortcuts import render, redirect
from django.contrib import messages
 
from .forms import TodoForm
from .models import Todo

def index(request):
    get_todo_data = Todo.objects.order_by("-date")
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Item Added")
            return redirect('todo-mainapp')
    form = TodoForm()
 
    page = {
             "forms" : form,
             "list" : get_todo_data,
             "title" : "TODO LIST Django App",
           }
    return render(request, 'mainapp/index.html', page)
 
 
def remove(request, item_id):
    item = Todo.objects.get(id=item_id)
    item.delete()
    messages.info(request, "Item Removed")
    return redirect('todo-mainapp')