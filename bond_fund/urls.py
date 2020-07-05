from .views.dashboard import (
    request_data_status,
    request_data,
    dashboard_charts
)
from django.conf.urls import url
from django.urls import path
from .views.usermanagement import (
    usermanagement_view,
    # add_user,
    change_user_status,
    usermanagement_trash,
    usermanagement_detail,
    user_add,
    add_user


)

from .views.profile import (
    profile_view,
    change_profile_info,
    profile_view_my,
    change_profile_info_my
)

from .views.staffdashboard import (
    staff_dashboard_view,
    request_data_status_staff,
    request_data_staff,
    all_transaction_view_staff,
    deduction_transaction_view_staff,
    saving_transaction_view_staff,
    add_request_staff,
    all_transaction_staff,
    saving_transaction_staff,
    view_transaction_staff,
    deduction_transaction_staff,


    all_request_view_staff,
    all_pending_view_staff,
    all_approve_view_staff,
    all_disapprove_view_staff,

    done_transaction_staff,
    create_transaction_staff,

)


from .views.userdashboard import (
    user_dashboard_view,
    request_data_status_user,
    request_data_user,
    all_transaction_view_user,
    deduction_transaction_view_user,
    saving_transaction_view_user

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
    # transactionsettings
    delete_transactionmanage,
    edit_transactionmanage,
    add_transactype,
    delete_ttype

)
from .views.transaction import (
    all_transaction_view,
    deduction_transaction_view,
    saving_transaction_view,
    create_transaction,
    done_transaction,
    view_transaction,

    # dashboard_view

)

from .views.request import (
    all_request_view,
    change_request_status,
    request_trash,
    add_request,
    load_transaction,
    view_request,
    all_pending_view,
    all_disapprove_view,
    all_approve_view,
    request_approve_checked,
    request_disapprove_checked,
    view_status_request

)
from .views.reports import (
    get_download_pdf,
    get_view_pdf,
    index_pdf,
    report_request_account,
    report_all_transaction,
    report_transaction_account,
    report_all_user,
    report_transaction_request_account
)


urlpatterns = [

    # profile
    path('profile', profile_view, name='profile'),
    path('my-profile', profile_view_my, name='my-profile'),

    path('change-profile-info', change_profile_info, name='change-profile-info'),
    path('change-profile-info-my', change_profile_info_my,
         name='change-profile-info-my'),

    # profile

    path('adduser', add_user, name='adduser'),
    path('add-user', user_add, name='add-user'),
    path('dashboard', dashboard_charts, name='dashboard'),
    path('request-data', request_data, name='request-data'),
    path('request-data-status', request_data_status, name='request-data-status'),



    url(r'^report-request-all$', get_view_pdf, name="report-request-all"),
    url(r'^generate-reports$', index_pdf, name="generate-reports"),
    url(r'^report-request-account/(?P<account_no>)$',
        report_request_account, name="report-request-account"),
    url(r'^report-all-transaction$', report_all_transaction,
        name="report-all-transaction"),
    url(r'^report-transaction-account/(?P<account_id>)$',
        report_transaction_account, name="report-transaction-account"),
    url(r'^report-all-user$', report_all_user, name="report-all-user"),
    url(r'^report-all-transaction-made/(?P<account_id>)$',
        report_transaction_request_account, name="report-all-transaction-made"),




    url(r'^get-download-pdf$',  get_download_pdf, name="get-download-pdf"),

    url(r'^user-management$', usermanagement_view, name='user-management'),
    # url(r'^add-user$', add_user, name='add-user'),
    url(r'^change-user-status$', change_user_status, name='change-user-status'),
    url(r'^usermanagement-trash$', usermanagement_trash,
        name='usermanagement-trash'),
    url(r'^usermanagement-detail$', usermanagement_detail,
        name='usermanagement-detail'),




    # Request Management
    url(r'^all-request$', all_request_view, name='all-request'),
    url(r'^change-request-status$', change_request_status,
        name='change-request-status'),
    url(r'^request-trash$', request_trash, name='request-trash'),

    url(r'^all-approve-request$', all_approve_view, name='all-approve-request'),
    url(r'^all-disapprove-request$', all_disapprove_view,
        name='all-disapprove-request'),

    url(r'^request-approve-checked$', request_approve_checked,
        name='request-approve-checked'),
    url(r'^request-disapprove-checked$', request_disapprove_checked,
        name='request-disapprove-checked'),


    url(r'^all-pending-request$', all_pending_view, name='all-pending-request'),

    url(r'^view-request$', view_request, name='view-request'),



    url(r'^view-status-request$', view_status_request, name='view-status-request'),
    url(r'^add-request$', add_request, name='add-request'),

    # url(r'^load-transaction$', load_transaction, name='load-transaction'),
    url(r'^load-transaction/(?P<id>\d+)$',
        load_transaction, name='load-transaction'),
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

    path('create-transaction/<request_no>', create_transaction),
    url(r'^view-transaction$', view_transaction, name='view-transaction'),

    url(r'^done-transaction$', done_transaction, name='done-transaction'),

    url(r'^all-transaction$', all_transaction_view, name='all-transaction'),
    url(r'^delete-transaction-manage$', delete_transactionmanage,
        name='delete-transaction-manage'),
    url(r'edit-transaction-manage$', edit_transactionmanage,
        name='edit-transaction-manage'),
    url(r'add-transactype$', add_transactype, name='add-transactype'),
    url(r'delete-ttype/(?P<id>\d+)$', delete_ttype, name='delete-ttype'),
    url(r'^deduction-transaction$',
        deduction_transaction_view, name='deduction-transaction'),
    url(r'^saving-transaction$',
        saving_transaction_view, name='savings-transaction'),


    url(r'^all-transaction-staff$', all_transaction_staff,
        name='all-transaction-staff'),
    url(r'^saving-transaction-staff$', saving_transaction_staff,
        name='saving-transaction-staff'),
    url(r'^view-transaction-staff$', view_transaction_staff,
        name='view-transaction-staff'),
    url(r'^deduction-transaction-staff$', deduction_transaction_staff,
        name='deduction-transaction-staff'),


    url(r'^all-request-view-staff$', all_request_view_staff,
        name='all-request-view-staff'),
    url(r'^all-pending-view-staff$', all_pending_view_staff,
        name='all-pending-view-staff'),
    url(r'^all-approve-view-staff$', all_approve_view_staff,
        name='all-approve-view-staff'),
    url(r'^all-disapprove-view-staff$', all_disapprove_view_staff,
        name='all-disapprove-view-staff'),

    url(r'^done-transaction-staff$', done_transaction_staff,
        name='done-transaction-staff'),
    path('create-transaction-staff/<request_no>', create_transaction_staff),


    url(r'^staff-dashboard$', staff_dashboard_view, name='staff-dashboard'),
    path('request-data-staff', request_data_staff, name='request-data-staff'),
    path('request-data-status-staff', request_data_status_staff,
         name='request-data-status-staff'),
    url(r'^my-all-transaction-staff$', all_transaction_view_staff,
        name='my-all-transaction-staff'),
    url(r'^my-deduction-transaction-staff$', deduction_transaction_view_staff,
        name='my-deduction-transaction-staff'),
    url(r'^my-saving-transaction-staff$', saving_transaction_view_staff,
        name='my-saving-transaction-staff'),
    url(r'^add-request-staff$', add_request_staff,
        name='add-request-staff'),


    url(r'^user-dashboard$', user_dashboard_view, name='user-dashboard'),
    path('request-data-user', request_data_user, name='request-data-user'),
    path('request-data-status-user', request_data_status_user,
         name='request-data-status-user'),
    url(r'^all-transaction-user$', all_transaction_view_user,
        name='all-transaction-user'),
    url(r'^deduction-transaction-user$', deduction_transaction_view_user,
        name='deduction-transaction-user'),
    url(r'^saving-transaction-user$', saving_transaction_view_user,
        name='saving-transaction-user'),






]
