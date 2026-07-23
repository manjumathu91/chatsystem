
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
import os

from groq import Groq

from django.conf import settings
from .forms import RegisterForm
from django.http import JsonResponse

import json


from .models import (
    Ticket,
    
    StaffProfile
)

from .forms import (
    TicketForm,
    MessageForm
)



# ==========================
# Home Page
# ==========================

def home(request):

    return render(
        request,
        "home.html"
    )



# ==========================
# Customer Ticket List
# ==========================

@login_required
def ticket_list(request):

    tickets = Ticket.objects.filter(
        user=request.user
    ).order_by("-created_at")


    context = {
        "tickets": tickets
    }


    return render(
        request,
        "support/ticket_list.html",
        context
    )



# ==========================
# Create Ticket
# ==========================

@login_required
def create_ticket(request):

    if request.method == "POST":

        form = TicketForm(request.POST)


        if form.is_valid():

            ticket = form.save(
                commit=False
            )


            ticket.user = request.user


            # Groq AI Priority
            # will be added here


            ticket.save()


            messages.success(
                request,
                "Support ticket created successfully."
            )


            return redirect(
                "ticket_detail",
                ticket.id
            )


    else:

        form = TicketForm()



    context = {
        "form": form
    }



    return render(
        request,
        "support/create_ticket.html",
        context
    )



# ==========================
# Ticket Detail + Chat
# ==========================

@login_required
def ticket_detail(request, ticket_id):


    ticket = get_object_or_404(
        Ticket,
        id=ticket_id
    )



    # Permission Check

    if ticket.user != request.user:


        if (
            ticket.assigned_to is None
            or
            ticket.assigned_to.user != request.user
        ):

            messages.error(
                request,
                "You don't have permission to view this ticket."
            )


            return redirect(
                "ticket_list"
            )



    ticket_messages = ticket.messages.all()



    if request.method == "POST":


        form = MessageForm(
            request.POST
        )


        if form.is_valid():


            message = form.save(
                commit=False
            )


            message.ticket = ticket


            message.user = request.user


            message.save()



            messages.success(
                request,
                "Message sent successfully."
            )


            return redirect(
                "ticket_detail",
                ticket.id
            )


    else:

        form = MessageForm()



    context = {

        "ticket": ticket,

        "messages_list": ticket_messages,

        "form": form

    }



    return render(
        request,
        "support/ticket_detail.html",
        context
    )



# ==========================
# Staff Dashboard
# ==========================

@login_required
def staff_dashboard(request):


    try:

        staff = StaffProfile.objects.get(
            user=request.user
        )


    except StaffProfile.DoesNotExist:


        messages.error(
            request,
            "You are not a staff member."
        )


        return redirect(
            "home"
        )



    tickets = Ticket.objects.filter(
        assigned_to__isnull=True
    ).order_by(
        "-created_at"
    )



    context = {

        "staff": staff,

        "tickets": tickets

    }



    return render(
        request,
        "support/staff_dashboard.html",
        context
    )



# ==========================
# Claim Ticket
# ==========================

@login_required
def claim_ticket(request, ticket_id):


    try:

        staff = StaffProfile.objects.get(
            user=request.user
        )


    except StaffProfile.DoesNotExist:


        messages.error(
            request,
            "Access denied."
        )


        return redirect(
            "home"
        )



    ticket = get_object_or_404(
        Ticket,
        id=ticket_id
    )



    if ticket.assigned_to:


        messages.warning(
            request,
            "Ticket already assigned."
        )


        return redirect(
            "staff_dashboard"
        )



    ticket.assigned_to = staff


    ticket.status = "In Progress"


    ticket.save()



    messages.success(
        request,
        "Ticket claimed successfully."
    )



    return redirect(
        "my_tickets"
    )



# ==========================
# Staff My Tickets
# ==========================

@login_required
def my_tickets(request):


    try:

        staff = StaffProfile.objects.get(
            user=request.user
        )


    except StaffProfile.DoesNotExist:


        messages.error(
            request,
            "Access denied."
        )


        return redirect(
            "home"
        )



    tickets = Ticket.objects.filter(
        assigned_to=staff
    ).order_by(
        "-created_at"
    )



    context = {

        "staff": staff,

        "tickets": tickets

    }



    return render(
        request,
        "support/my_tickets.html",
        context
    )

# ==========================
# User Registration
# ==========================

# ==========================
# User Registration
# ==========================

def register(request):

    if request.method == "POST":

        form = RegisterForm(
            request.POST
        )


        if form.is_valid():

            user = form.save()


            login(
                request,
                user
            )


            messages.success(
                request,
                "Account created successfully."
            )


            return redirect(
                "home"
            )


    else:

        form = RegisterForm()



    context = {

        "form": form

    }


    return render(

        request,

        "registration/register.html",

        context

    )
# ==========================
# User Profile
# ==========================

@login_required
def profile(request):


    return render(
        request,
        "registration/profile.html"
    )



# ==========================
# Chatbot Page
# ==========================

@login_required
def chatbot(request):


    return render(
        request,
        "support/chatbot.html"
    )



# ==========================
# FAQ Page
# ==========================

def faq(request):


    return render(
        request,
        "support/faq.html"
    )



# ==========================
# AI FAQ Answer
# ==========================


# ==========================
# AI FAQ Answer - Groq
# ==========================

def get_faq_answer(request):

    if request.method == "POST":

        data = json.loads(
            request.body
        )

        question = data.get(
            "question"
        )


        try:

            client = Groq(
                api_key=settings.GROQ_API_KEY
            )


            response = client.chat.completions.create(

                model="llama-3.3-70b-versatile",


                messages=[

                    {
                        "role": "system",
                        "content":
                        """
                        You are a helpful customer support assistant.
                        Answer user questions clearly and politely.
                        Help with account, payment, ticket and technical issues.
                        """
                    },


                    {
                        "role": "user",
                        "content": question
                    }

                ],

                temperature=0.5

            )


            answer = response.choices[0].message.content



            return JsonResponse({

                "answer": answer

            })


        except Exception as e:


            return JsonResponse({

                "answer":
                "AI service temporarily unavailable.",

                "error": str(e)

            })



    return JsonResponse({

        "error": "Invalid request"

    })

# ==========================
# About Page
# ==========================

def about(request):


    return render(
        request,
        "support/about.html"
    )



# ==========================
# Contact Page
# ==========================

def contact(request):


    return render(
        request,
        "support/contact.html"
    )