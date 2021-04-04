from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from advertisements.models import Advertisement
from .forms import ContactForm
from .models import Contact


@login_required
def contact(request, pk):
    advertisement = None
    recipient = User.objects.get(id=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            sender = request.user
            new_contact = Contact(recipient=recipient,
                                  advertisement=advertisement,
                                  message=message,
                                  phone=phone,
                                  email=email,
                                  sender=sender)
            new_contact.save()
            messages.success(request, 'Medling sendt!')
            return redirect('ads')
    else:
        form = ContactForm(initial={'email': request.user.email})
    context = {'form': form, 'recipient':recipient, 'title':'contact'}
    return render(request, 'contact.html', context)
