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



def manage_inventory(request):
    inventory = Item.objects.all()  # Fetch all items from the database
    return render(request, 'manage_inventory.html', {'inventory': inventory})

def inventory(request):
    items = Item.objects.all()
    return render(request, 'inventory.html', {'items': items})

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
    message = None  # To store success or error message
    if request.method == 'POST':
        try:
            item_id = request.POST.get('item_id')
            quantity_taken = int(request.POST.get('quantity'))

            # Fetch the item from the database
            item = Item.objects.get(id=item_id)

            # Ensure there are enough items to take
            if item.count >= quantity_taken:
                # Update the quantity
                item.count -= quantity_taken
                item.save()
                message = "Item taken successfully!"
            else:
                message = "Not enough stock available."

        except Item.DoesNotExist:
            message = "Item not found."

        except ValueError:
            message = "Invalid quantity entered."

        except Exception as e:
            message = f"An error occurred: {str(e)}"

    items = Item.objects.all()
    return render(request, 'take_item.html', {'items': items, 'message': message})






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

        item = get_object_or_404(Item, id=item_id)
        item.count += quantity
        item.save()

        # Record the transaction
        Transaction.objects.create(
            item=item,
            quantity=quantity,
            action='return',
            user_name=user_name,
            date=date
        )

        messages.success(request, f'{quantity} {item.name}(s) returned successfully.')
        return redirect('transaction')

    items = Item.objects.all()
    return render(request, 'return_item.html', {'items': items})


def home(request):
    return render(request, 'home.html')  # Render home.html template


from django.shortcuts import render
from django.http import JsonResponse
from .models import Item


def get_inventory(request):
    # Fetch all items
    inventory = Item.objects.all()


    data = [
        {
            "image": item.image.url if item.image else '',
            "name": item.name,
            "quantity": item.count
        }
        for item in inventory
    ]


    if request.is_ajax():
        return JsonResponse(data, safe=False)


    return render(request, 'inventory.html', {'inventory_data': data})

def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    # Add logic for handling the edit form (GET and POST requests)
    return render(request, 'edit_item.html', {'item': item})



def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        item.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)
