from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [

    # =====================
    # Home
    # =====================

    path(
        "",
        views.home,
        name="home"
    ),



    # =====================
    # Authentication
    # =====================

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login"
    ),


    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),



    path(
        "register/",
        views.register,
        name="register"
    ),


    path(
        "profile/",
        views.profile,
        name="profile"
    ),



    # =====================
    # Customer Tickets
    # =====================


    path(
        "tickets/",
        views.ticket_list,
        name="ticket_list"
    ),



    path(
        "ticket/create/",
        views.create_ticket,
        name="create_ticket"
    ),



    path(
        "ticket/<int:ticket_id>/",
        views.ticket_detail,
        name="ticket_detail"
    ),



    # =====================
    # Staff Section
    # =====================


    path(
        "staff-dashboard/",
        views.staff_dashboard,
        name="staff_dashboard"
    ),



    path(
        "claim-ticket/<int:ticket_id>/",
        views.claim_ticket,
        name="claim_ticket"
    ),



    path(
        "my-tickets/",
        views.my_tickets,
        name="my_tickets"
    ),



    # =====================
    # AI Support
    # =====================


    path(
        "chatbot/",
        views.chatbot,
        name="chatbot"
    ),



    path(
        "faq/",
        views.faq,
        name="faq"
    ),



    path(
        "faq-answer/",
        views.get_faq_answer,
        name="get_faq_answer"
    ),



    # =====================
    # Static Pages
    # =====================


    path(
        "about/",
        views.about,
        name="about"
    ),



    path(
        "contact/",
        views.contact,
        name="contact"
    ),

]