"""
common functions for the api
"""
import csv
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from decouple import config

from django.db import transaction
from ..models import Transaction

# pylint: disable=no-member


def get_file_path():
    """
    get the path of the specific file
    :return: path of the file
    """
    return os.path.dirname(os.path.abspath(__file__))


def get_message_path():
    """
    :return: the message file path error
    """
    return os.path.join(get_file_path(), 'messages')


def get_email_path():
    """
    get the email file path
    :return: the email file path
    """
    return os.path.join(get_file_path(), 'emails')


def get_template_html(body_input, body_is_filename=True, path=get_email_path()):
    """
        Args:
            body_is_filename: Boolean
            body_input: filename or text body.
            path: either to message or email
        Returns:
    """
    if body_is_filename:
        try:
            with open(os.path.join(path, body_input), encoding='utf-8') as fp:
                html = fp.read()
                return html
        except FileNotFoundError:  # tries on both folders, emails and messages
            with open(os.path.join(get_message_path(), body_input), encoding='utf-8') as fp:
                return fp.read()
    else:
        return body_input


def send_email(subject, sender_email, recipient_email, path_summary_info_file):
    """
    send an email with the all information of the stori card
    :param subject:
    :param sender_email:
    :param recipient_email:
    :param path_summary_info_file:
    :return: none
    """
    msg = MIMEMultipart()
    msg['subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    html = get_template_html(body_input='stori_transactions_info.html')
    msg.attach(MIMEText(html, 'html'))
    attachment = get_attachment(path_summary_info_file)
    if attachment:
        msg.attach(attachment)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, config('email_password'))
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()
    os.remove(path_summary_info_file)


def create_csv_file(summary_info):
    """
    create csv file with summary information
    :param summary_info:
    :return:
    """
    field_names = ['total_balance', 'Month', 'Number of Transactions', 'Average Debit', 'Average Credit']
    file_path = 'summary_info.csv'
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            first_month = True
            for month_data in summary_info['detailed_info']:
                if first_month:
                    writer.writerow({
                        'total_balance': summary_info['total_balance'],
                        'Month': month_data['month'],
                        'Number of Transactions': month_data['num_transactions'],
                        'Average Debit': abs(month_data['avg_debit']),
                        'Average Credit': month_data['avg_credit']
                    })
                    first_month = False
                else:
                    writer.writerow({
                        'total_balance': '',
                        'Month': month_data['month'],
                        'Number of Transactions': month_data['num_transactions'],
                        'Average Debit': abs(month_data['avg_debit']),
                        'Average Credit': month_data['avg_credit']
                    })
        return os.path.abspath(file_path)
    except IOError:
        return None


def get_attachment(file_path):
    """
    Get attachment
    :param file_path:
    :return:
    """
    try:
        with open(file_path, 'rb') as file:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition',
                                  f'attachment; filename={os.path.basename(file_path)}')
            return attachment
    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no fue encontrado.")
        return None


def save_csv_info(card_transactions):
    """
    Save data inside the database
    :param card_transactions:
    :return:
    """
    transaction_objects = [Transaction(date=card['date'], transaction=card['transaction'])
                           for card in card_transactions]
    with transaction.atomic():
        Transaction.objects.bulk_create(transaction_objects, batch_size=100)
