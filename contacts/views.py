from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact


@login_required
def contact(request, pk):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            recipient_id = pk
            message = form.cleaned_data['message']
            sender_id = request.user.id
            new_contact = Contact(recipient_id=recipient_id,
                                  message=message,
                                  sender_id=sender_id)
            new_contact.save()
            messages.success(request, 'Medling sendt!')
            return redirect('ads')
    else:
        form = ContactForm()
    recipient = User.objects.get(id=pk)
    return render(request, 'contact.html', {'form': form, 'recipient':recipient})