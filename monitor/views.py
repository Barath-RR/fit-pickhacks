from django.shortcuts import render

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
