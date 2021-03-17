from rest_framework import serializers
from bond_fund.models import Requests
from rest_framework.serializers import ModelSerializer


class RequestsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requests
        fields = ['id', 'request_no',
         'account_no', 'status',
         'amount', 'remark', 'clerk',
          'trash', 'date_created',
          'date_modified', 'transaction_id']
