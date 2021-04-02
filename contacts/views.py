from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from advertisements.models import Advertisement
from .forms import ContactForm
from .models import Contact


@login_required
def contact(request, pk):
    recipient = Advertisement.objects.get(id=pk).author
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            advertisement_id = pk
            recipient_id = recipient.id
            message = form.cleaned_data['message']
            sender_id = request.user.id
            new_contact = Contact(recipient_id=recipient_id,
                                  advertisement_id=advertisement_id,
                                  message=message,
                                  sender_id=sender_id)
            new_contact.save()
            messages.success(request, 'Medling sendt!')
            return redirect('ads')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, 'recipient':recipient})