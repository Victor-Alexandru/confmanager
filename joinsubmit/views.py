from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required()
def view_conferences(request):
    return render(request, 'joinsubmit/available_conf.html', {})

def submit_view(request):
    return render(request, 'joinsubmit/add_abstract.html',{})
