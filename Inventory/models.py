from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='', blank=True)  # Empty string instead of null
    count = models.IntegerField(default=0)  # Default value of 0 to prevent negative stock
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)  # Keeping null=True for optional image

    def __str__(self):
        return self.name

    def update_count(self, quantity):
        """Helper method to update item count."""
        if self.count + quantity < 0:
            raise ValueError("Cannot have negative count")
        self.count += quantity
        self.save()


class Transaction(models.Model):
    ACTIONS = (
        ('take', 'Take'),
        ('return', 'Return'),
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    action = models.CharField(max_length=10, choices=ACTIONS)
    quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)  # Automatically set the date when the transaction is created

    def __str__(self):
        return f"{self.user_name} - {self.action} {self.item.name}"
