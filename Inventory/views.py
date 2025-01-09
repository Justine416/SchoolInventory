import json
from .models import Item, Transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse





def is_admin(user):
    if not user.is_staff:
        return redirect('manage_inventory')
    return True




def inventory(request):
    # Fetch inventory data from the database or use static data
    items = Item.objects.all()
    return render(request, 'inventory.html', {'items': items})

def manage_inventory(request):
    # Fetch inventory data for managing
    items = Item.objects.all()
    return render(request, 'manage_inventory.html', {'items': items})

def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        count = request.POST.get('count')
        description = request.POST.get('description')  # Handle description
        image = request.FILES.get('image')  # Handle image upload

        # Validation
        if not name or not count.isdigit() or int(count) < 0:
            return render(request, 'add_item.html', {'error': 'Invalid input. Please try again.'})

        # Create the item
        Item.objects.create(
            name=name,
            description=description,  # Ensure description is saved
            count=int(count),
            image=image
        )
        messages.success(request, 'Item added successfully!')
        return redirect('inventory')  # Redirect back to the inventory page

    return render(request, 'add_item.html')

def manage_transaction(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        quantity = request.POST.get('quantity')
        date = request.POST.get('date')

        # Validation for quantity
        if not quantity.isdigit() or int(quantity) <= 0:
            messages.error(request, 'Invalid quantity. Please enter a positive number.')
            return redirect('inventory')

        quantity = int(quantity)

        # Retrieve the item
        item = get_object_or_404(Item, id=item_id)

        if action == 'take':
            if item.count >= quantity:
                item.count -= quantity
            else:
                messages.error(request, 'Not enough stock to take this quantity.')
                return redirect('inventory')
        elif action == 'return':
            item.count += quantity
        else:
            messages.error(request, 'Invalid action. Please try again.')
            return redirect('inventory')

        item.save()

        # Log the transaction
        Transaction.objects.create(
            item=item, user_name=user_name, action=action, quantity=quantity, date=date
        )

        messages.success(request, f'Transaction completed: {action.capitalize()} {quantity} {item.name}(s).')
        return redirect('inventory')

    return redirect('inventory')


def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-date')  # Latest transactions first
    return render(request, 'transaction.html', {'transactions': transactions})



@csrf_exempt
def take_item(request):
    if request.method == 'POST':
        # Get data from the form
        user_name = request.POST['user_name']
        item_id = request.POST['item_id']
        quantity = int(request.POST['quantity'])
        date = request.POST['date']

        # Find the item being taken
        item = Item.objects.get(id=item_id)

        # Check if enough quantity is available
        if item.count >= quantity:  # Use item.count instead of item.stock
            # Process the transaction
            item.count -= quantity  # Reduce the inventory count
            item.save()

            # Create a new transaction record
            transaction = Transaction(
                user_name=user_name,
                item=item,
                quantity=quantity,
                date=date,
                action='take'  # You can define whether it's a 'take' or 'return'
            )
            transaction.save()

            # Add a success message for the user
            messages.success(request, f'{quantity} {item.name}(s) successfully taken!')

            # Redirect to a confirmation page or reload the page
            return redirect('transaction_list')
        else:
            # Show an error if there is not enough stock
            messages.error(request, 'Not enough stock available for this item.')

    items = Item.objects.all()  # Retrieve all items for the form
    return render(request, 'take_item.html', {'items': items})


def return_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = request.POST.get('quantity')
        user_name = request.POST.get('user_name')
        date = request.POST.get('date')

        # Validation for quantity
        if not quantity.isdigit() or int(quantity) <= 0:
            messages.error(request, 'Invalid quantity. Please enter a positive number.')
            return redirect('return_item')

        quantity = int(quantity)

        # Find the item being returned
        item = get_object_or_404(Item, id=item_id)

        # Update the stock count of the item
        item.count += quantity
        item.save()

        # Record the return transaction
        Transaction.objects.create(
            item=item,
            quantity=quantity,
            action='return',
            user_name=user_name,
            date=date
        )

        # Success message
        messages.success(request, f'{quantity} {item.name}(s) returned successfully.')

        # Clear transaction table (optional)
        # Transaction.objects.filter(action='return', item=item, quantity=quantity).delete()  # Uncomment if you want to delete it after return

        return redirect('transaction_list')

    items = Item.objects.all()
    return render(request, 'return_item.html', {'items': items})




def home(request):
    return render(request, 'home.html')  # Render home.html template

def get_inventory(request):
    items = Item.objects.all()
    data = []
    for item in items:
        data.append({
            'id': item.id,
            'name': item.name,
            'image_url': item.image.url if item.image else '',  # Check if item has an image
            'quantity': item.count,
        })
    return JsonResponse({'items': data})


def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    # Add logic for handling the edit form (GET and POST requests)
    return render(request, 'edit_item.html', {'item': item})



def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        item.delete()
        # Redirect to manage_inventory page after deletion
        return redirect('manage_inventory')  # Ensure 'manage_inventory' is the name of the URL pattern

    # Handle invalid request method
    return JsonResponse({'error': 'Invalid request method'}, status=400)
