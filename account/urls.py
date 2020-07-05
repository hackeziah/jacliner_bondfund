from django.conf.urls import url
from django.urls import path
from .views import (login_view,
                    registration_view,
                    logout_view,
                    admin_dashboard_view,
                    # user_dashboard_view,
                    # staff_dashboard_view
                    )

urlpatterns = [
    url(r'^logout$', logout_view, name='logout'),
    url(r'^login$', login_view, name='login'),
    url(r'^$', login_view, name='login'),
    url(r'^registration$', registration_view, name='registration'),
    url(r'^admin-dashboard$',
        admin_dashboard_view, name='admin-dashboard'),
    # url(r'^user-dashboard$',
    #     user_dashboard_view, name='user-dashboard'),
    # url(r'^staff-dashboard$', staff_dashboard_view, name='staff-dashboard')
]
