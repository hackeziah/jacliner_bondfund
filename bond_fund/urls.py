from django.conf.urls import url
from django.urls import path
from .views.usermanagement import (
    usermanagement_view

)
from .views.settings import (
    transaction_view,
    company_view,
    position_view,
    # company cred
    add_company,
    delete_company,
    edit_company,
    # position route
    delete_postion,
    edit_postion,
    add_position,
    #transactionsettings
    delete_transactionmanage,
    edit_transactionmanage,
    add_transactype,
    delete_ttype

)
from .views.transaction import (
    all_transaction_view,
    deduction_transaction_view,
    saving_transaction_view
    # dashboard_view

)

from .views.request import (
    all_request_view,
    change_request_status,
    request_trash,
    add_request,
    load_transaction,
    view_request

)
# from .views.staffdashboard import (
#     # staff_dashboard_view,
# )


urlpatterns = [

    url(r'^user-management$', usermanagement_view, name='user-management'),
    #Request Management
    url(r'^all-request$', all_request_view, name='all-request'),
    url(r'^change-request-status$', change_request_status, name='change-request-status'),
    url(r'^request-trash$', request_trash, name='request-trash'),

    url(r'^view-request$', view_request, name='view-request'),

    url(r'^add-request$', add_request, name='add-request'),
    # url(r'^load-transaction$', load_transaction, name='load-transaction'),
    url(r'^load-transaction/(?P<id>\d+)$',load_transaction, name='load-transaction'),
    url(r'^add-company$', add_company, name='add-company'),
    url(r'^delete-company$',
        delete_company, name='delete-company'),
    url(r'^edit-company$',
        edit_company, name='edit-company'),

    url(r'^transaction-setup$', transaction_view, name='transaction-setup'),
    url(r'^company-setup$', company_view, name='company-setup'),
    url(r'^position-setup$', position_view, name='position-setup'),

    url(r'^delete-position$', delete_postion, name='delete-position'),
    url(r'^edit-position$', edit_postion, name='edit-position'),
    url(r'^add-position$', add_position, name='add-position'),

    url(r'^all-transaction$', all_transaction_view, name='all-transaction'),
    url(r'^delete-transaction-manage$', delete_transactionmanage, name='delete-transaction-manage'),
    url(r'edit-transaction-manage$', edit_transactionmanage, name='edit-transaction-manage'),
    url(r'add-transactype$', add_transactype, name='add-transactype'),
    url(r'delete-ttype/(?P<id>\d+)$', delete_ttype, name='delete-ttype'),
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
