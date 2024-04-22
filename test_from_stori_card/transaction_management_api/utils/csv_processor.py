"""
    proccess of csv file
"""
import csv
import datetime
import io
from decimal import Decimal

from django.db.models import Count, Sum, Avg, Q, DateField
from django.db.models.functions import TruncMonth
from rest_framework.response import Response

from ..models import Transaction


# pylint: disable=no-member

class CSVProcessor:
    """
        CSVProcessor using the Singleton pattern to process the CSV file and generate the summary:
    """
    _instance = None

    @staticmethod
    def get_instance():
        """
        :return: the instance
        """
        if not CSVProcessor._instance:
            CSVProcessor._instance = CSVProcessor()
        return CSVProcessor._instance

    @staticmethod
    def process(csv_file):
        """
        This method reads the .csv file, processes it and reconstructs the information from this file to be
        stored in the db
        :param csv_file:
        :return:
        """
        transactions = []
        try:
            csv_data = csv_file.read()
            if not isinstance(csv_data, str):
                csv_data = csv_data.decode('utf-8')
            csv_io = io.StringIO(csv_data)
            reader = csv.DictReader(csv_io)
            for row in reader:
                date_str = row['date']
                date_obj = datetime.datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
                transaction = {
                    'date': date_obj,
                    'transaction': float(row['transaction'])
                }
                transactions.append(transaction)
        except FileNotFoundError as e:
            return Response(f"Error processing CSV file: {e}", status=400)
        return transactions

    @staticmethod
    def generate_summary():
        """
        method that reconstructs the information to send it to a file.csv for an email
        :return:
        """
        try:
            total_balance_cache = Transaction.objects.aggregate(total_balance=Sum('transaction'))['total_balance']
            monthly_summary = Transaction.objects.prefetch_related('related_model').annotate(
                month=TruncMonth('date', output_field=DateField())
            ).values('month').annotate(
                num_transactions=Count('id'),
                avg_debit=Avg('transaction', filter=Q(transaction__lt=0)),
                avg_credit=Avg('transaction', filter=Q(transaction__gt=0))
            ).order_by('month')

            formatted_info = []
            for item in monthly_summary:
                month_name = item['month'].strftime('%B')
                formatted_info.append({
                    'month': month_name,
                    'num_transactions': item['num_transactions'],
                    'avg_debit': float(item['avg_debit'].quantize(Decimal('0.01'))),
                    'avg_credit': float(item['avg_credit'].quantize(Decimal('0.01')))
                })

            summary_info = {
                'total_balance': float(total_balance_cache) if total_balance_cache is not None else 0,
                'detailed_info': formatted_info
            }
            return summary_info
        except ValueError as e:
            print(f"Error generating summary: {e}")
            return None
