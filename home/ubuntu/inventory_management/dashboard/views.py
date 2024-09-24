from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventory.models import Store, InventoryItem
from django.db.models import Sum
from django.utils import timezone

@login_required
def store_manager_dashboard(request):
    store = Store.objects.filter(client=request.user.client).first()

    # Current stock levels
    stock_levels = InventoryItem.objects.filter(store=store).values('name').annotate(total_quantity=Sum('quantity'))

    # Daily sales report
    today = timezone.now().date()
    daily_sales = InventoryItem.objects.filter(store=store, updated_at__date=today).values('name').annotate(total_sold=Sum('quantity'))

    # Unauthorized events log (placeholder - implement actual event logging)
    unauthorized_events = []

    context = {
        'stock_levels': stock_levels,
        'daily_sales': daily_sales,
        'unauthorized_events': unauthorized_events,
    }
    return render(request, 'dashboard/store_manager.html', context)

@login_required
def admin_dashboard(request):
    # Aggregate data across all stores
    total_stock = InventoryItem.objects.values('name').annotate(total_quantity=Sum('quantity'))

    # Total sales across all stores (placeholder - implement actual sales tracking)
    total_sales = InventoryItem.objects.values('name').annotate(total_sold=Sum('quantity'))

    # License management (placeholder - implement actual license management)
    licenses = Store.objects.all()

    context = {
        'total_stock': total_stock,
        'total_sales': total_sales,
        'licenses': licenses,
    }
    return render(request, 'dashboard/admin.html', context)
