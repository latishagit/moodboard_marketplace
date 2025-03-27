from .models import Category  # Import the Category model

def categories_context(request):
    return {
        'categories': Category.objects.all()  # Fetch all categories globally
    }

