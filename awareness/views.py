from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def contacts(request):
    return render(request, 'contacts.html')

def exercises(request):
    return render(request, 'exercises.html')

def healthy_diets(request):
    return render(request, 'healthy_diets.html')

def prevention(request):
    return render(request, 'prevention.html')

def services(request):
    return render(request, 'services.html')

def water(request):
    return render(request, 'water.html')

def fast(request):
    return render(request, 'fast.html')

def diabetes(request):
    return render(request, 'diabetes.html')

def impact(request):
    return render(request, 'negativeDiabetes.html')

def heart(request):
    return render(request, 'heart.html')

def eyes(request):
    return render(request,'eyes.html')

def kidney(request):
    return render(request,'kidney.html')

def nerves(request):
    return render(request, 'nerves.html')


def digestion(request):
    return render(request, 'digestion.html')

def skin(request):
    return render(request, 'skin.html')

def privacy(request):
    return render(request, 'privacy.html')

def conditions(request):
    return render(request, 'conditions.html')

