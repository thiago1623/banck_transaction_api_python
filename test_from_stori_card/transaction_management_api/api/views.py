"""
Views for transaction management
"""
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TransactionSerializer
from ..models import Transaction
from ..utils.csv_processor import CSVProcessor
from ..utils.email_sender import EmailSender
from ..utils import common

# pylint: disable=no-member


class TransactionListView(APIView):
    """
    List all transactions
    """
    def get(self, request):  # pylint: disable=unused-argument
        """
        :param request:
        :return: all transactions
        """
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class SetCardTransactionDataViewSet(APIView):
    """
        this endpoint is used to set the card transaction data from the card
        receives the file .csv and save all data in the database
        then send email to user with the data info
    """
    def post(self, request):
        """
        :param request:
        :return: the response of the post request
        """
        if 'file' not in request.FILES:
            return Response({"error": "File not found in request"}, status=400)
        csv_file = request.FILES['file']
        csv_processor = CSVProcessor.get_instance()
        card_transactions = csv_processor.process(csv_file)
        if card_transactions:
            common.save_csv_info(card_transactions)
        summary_info = CSVProcessor.generate_summary()
        EmailSender.send_summary_email(summary_info)
        return JsonResponse({"message": "File processed successfully, and email sent successfully"}, status=200)
