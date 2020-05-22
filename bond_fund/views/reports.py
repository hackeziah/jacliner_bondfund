from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from bond_fund.models import *
import datetime


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	# filename = "Invoice_%s.pdf" %("12341231")
	# response['Content-Disposition'] = filename
	result = BytesIO()

	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

def get_view_pdf(request):
	thead = ["Request Number","Account Number","Amount","Type","Status","Realese By","Date"]
	objects = Requests.objects.filter(trash=0)
	date = datetime.datetime.now()
	data = {
			'title': "Report All Requests",
			'objects': objects,
			'thead' : thead,
			'date' : date
	}
	pdf = render_to_pdf('report/request_reports.html', data)
	return HttpResponse(pdf, content_type='application/pdf')

def report_request_account(request,account_no):

	if request.method == "GET":
		account_no = request.GET.get('account_no',None)
		thead = ["Request Number","Amount","Type","Status","Realese By","Date"]
		objects = Requests.objects.filter(trash=0,account_no = str(account_no))
		date = datetime.datetime.now()
		account_no=str(account_no)
		data = {
				'title': "Report All Requests by " + account_no,
				'objects': objects,
				'thead' : thead,
				'date' : date
		}
		pdf = render_to_pdf('report/request_report_account.html', data)
		return HttpResponse(pdf, content_type='application/pdf')
	else:
		return HttpResponseRedirect('/generate-reports')


def get_download_pdf(request):
	data = Requests.objects.filter(trash=0)
	pdf = render_to_pdf('report/request_template.html', data)
	response = HttpResponse(pdf, content_type='application/pdf')
	filename = "Invoice_%s.pdf" %("12341231")
	content = "attachment; filename='%s'" %(filename)
	response['Content-Disposition'] = content
	return response



def index_pdf(request):
	contentheader = "Generate Reports"
	title = "Generate Reports"
	content = {
        'title': title,
        'contentheader': contentheader,
        # 'data' : data,
    }

	return render(request, 'report/index.html', content)
