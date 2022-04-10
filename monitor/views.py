from django.shortcuts import redirect, render
from .models import dietm
def monitor(request):
    return render(request, 'cam.html')
def landing(request):
    return render(request,"index.html")
def leader(request):
    return render(request,"leader.html")
def tournment(request):
    return render(request,"tournament.html")
def card(request):
    return render(request,"card.html")
def card_eight(request):
    return render(request,"card_eight.html")

def diet(request):
    return render(request,"diet.html")

def about(request):
    return render(request,"aboutus.html")

def form(request):
    if request.method == "POST":
        dietm.objects.create(
            age=request.POST.get("age"),
            weight=request.POST.get('weight'),
            diet_type=request.POST.get('dt')
        )
        return redirect("/diet")
        
    return render(request,"form.html")
