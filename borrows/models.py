from django.db import models

class Borrow(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]

    user_id = models.IntegerField()
    book_id = models.IntegerField()
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='borrowed',
    )
    extend_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user_id + ' - ' + self.book_id