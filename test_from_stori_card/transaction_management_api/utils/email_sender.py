"""
Email Sender
"""
from decouple import config
from .common import send_email, create_csv_file


class EmailSender:
    """
    Using the Singleton pattern to send the summary email
    """
    _instance = None

    @staticmethod
    def get_instance():
        """ get the singleton instance """
        if not EmailSender._instance:
            EmailSender._instance = EmailSender()
        return EmailSender._instance

    @staticmethod
    def send_summary_email(summary_info):
        """generates the summary for the email to be sent in a .csv file"""
        path_summary_info_file = create_csv_file(summary_info)
        if path_summary_info_file:
            subject = "information about your financial status with stori card"
            send_email(subject, config('sender_email'),
                       config('recipient_email'), path_summary_info_file)
