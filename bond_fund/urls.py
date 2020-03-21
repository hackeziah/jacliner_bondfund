from django.conf.urls import url
from django.urls import path
from .views.usermanagement import (
    usermanagement_view

)
from .views.settings import (
    deduction_view,
    company_view,
    position_view,


)
from .views.transaction import (
    all_transaction_view,
    deduction_transaction_view,
    saving_transaction_view
    # dashboard_view

)
# from .views.userdashboard import (
#     # user_dashboard_view,
# )
# from .views.staffdashboard import (
#     # staff_dashboard_view,
# )


urlpatterns = [
    url(r'^user-management$', usermanagement_view, name='user-management'),
    url(r'^deduction-setup$', deduction_view, name='deduction-setup'),
    url(r'^company-setup$', company_view, name='company-setup'),
    url(r'^position-setup$', position_view, name='position-setup'),
    url(r'^all-transaction$', all_transaction_view, name='all-transaction'),
    url(r'^deduction-transaction$',
        deduction_transaction_view, name='deduction-transaction'),
    url(r'^saving-transaction$',
        saving_transaction_view, name='savings-transaction')
    # url(r'^dashboard$',
    #     dashboard_view, name='dashboard'),
    # url(r'^user-dashboard$',
    #     user_dashboard_view, name='user-dashboard'),
    # url(r'^staff-dashboard$', staff_dashboard_view, name='staff-dashboard'),


]
