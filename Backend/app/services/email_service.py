import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

logger = logging.getLogger(__name__)


def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """
    Send HTML Email via SMTP.
    If SMTP parameters are missing (e.g. in dev), log cleanly and return True without crashing.
    """
    if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
        logger.info(f"[EMAIL DEV MODE] Suppressed email to '{to_email}' with subject '{subject}'")
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.FROM_EMAIL or settings.SMTP_USERNAME
        msg["To"] = to_email

        part = MIMEText(html_content, "html")
        msg.attach(part)

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(msg["From"], [to_email], msg.as_string())
        
        logger.info(f"Email successfully sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False


def send_admin_enquiry_notification(enquiry_data: dict):
    subject = f"New Vidwan Classes Enquiry: {enquiry_data.get('name')} ({enquiry_data.get('enquiry_type', 'general')})"
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.6; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; }}
            .header {{ background-color: #0b1f3a; color: #ffffff; padding: 15px; border-radius: 6px 6px 0 0; font-size: 18px; font-weight: bold; }}
            .content {{ padding: 20px; background-color: #f9fbfd; }}
            .field {{ margin-bottom: 12px; }}
            .label {{ font-weight: bold; color: #0056b3; }}
            .footer {{ font-size: 12px; color: #777; margin-top: 20px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">🎓 New Website Enquiry Received</div>
            <div class="content">
                <div class="field"><span class="label">Name:</span> {enquiry_data.get('name')}</div>
                <div class="field"><span class="label">Email:</span> {enquiry_data.get('email', 'N/A')}</div>
                <div class="field"><span class="label">Phone:</span> {enquiry_data.get('phone')}</div>
                <div class="field"><span class="label">Course Interested:</span> {enquiry_data.get('course', 'N/A')}</div>
                <div class="field"><span class="label">Source Form:</span> {enquiry_data.get('source', 'Website')}</div>
                <div class="field"><span class="label">Enquiry Type:</span> {enquiry_data.get('enquiry_type', 'general')}</div>
                <div class="field"><span class="label">Message:</span><br>{enquiry_data.get('message', 'No message provided')}</div>
            </div>
            <div class="footer">Vidwan Classes Automated Enquiry System</div>
        </div>
    </body>
    </html>
    """
    send_email(settings.ADMIN_EMAIL, subject, html_content)


def send_user_enquiry_acknowledgement(user_email: str, user_name: str):
    if not user_email:
        return
    subject = "Thank you for contacting Vidwan Classes!"
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.6; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; }}
            .header {{ background-color: #0b1f3a; color: #ffffff; padding: 15px; border-radius: 6px 6px 0 0; font-size: 18px; font-weight: bold; }}
            .content {{ padding: 20px; background-color: #ffffff; }}
            .footer {{ font-size: 12px; color: #777; margin-top: 20px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">Welcome to Vidwan Classes</div>
            <div class="content">
                <p>Dear <strong>{user_name}</strong>,</p>
                <p>Thank you for reaching out to Vidwan Classes. We have received your request and our academic counselor will contact you shortly.</p>
                <p>If you have urgent questions, feel free to call us directly at <strong>+91 98765 43210</strong>.</p>
                <br>
                <p>Best regards,<br><strong>Vidwan Classes Team</strong></p>
            </div>
            <div class="footer">Empowering Scholars. Engineering Success.</div>
        </div>
    </body>
    </html>
    """
    send_email(user_email, subject, html_content)


def send_vst_registration_notification(vst_data: dict):
    # Admin notification
    subject = f"New VST Registration: {vst_data.get('student_name')} (Class {vst_data.get('class_name')})"
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.6; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; }}
            .header {{ background-color: #d97706; color: #ffffff; padding: 15px; border-radius: 6px 6px 0 0; font-size: 18px; font-weight: bold; }}
            .content {{ padding: 20px; background-color: #fffbeb; }}
            .field {{ margin-bottom: 10px; }}
            .label {{ font-weight: bold; color: #92400e; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">🏆 New VST Scholarship Registration</div>
            <div class="content">
                <div class="field"><span class="label">Student Name:</span> {vst_data.get('student_name')}</div>
                <div class="field"><span class="label">Parent Name:</span> {vst_data.get('parent_name', 'N/A')}</div>
                <div class="field"><span class="label">Email:</span> {vst_data.get('email')}</div>
                <div class="field"><span class="label">Phone:</span> {vst_data.get('phone')}</div>
                <div class="field"><span class="label">Class:</span> {vst_data.get('class_name')}</div>
                <div class="field"><span class="label">School:</span> {vst_data.get('school', 'N/A')}</div>
                <div class="field"><span class="label">Preferred Center:</span> {vst_data.get('preferred_center', 'N/A')}</div>
                <div class="field"><span class="label">Exam Target:</span> {vst_data.get('exam_type', 'N/A')}</div>
            </div>
        </div>
    </body>
    </html>
    """
    send_email(settings.ADMIN_EMAIL, subject, html_content)
    
    # User notification
    if vst_data.get("email"):
        user_subject = "VST Registration Confirmation — Vidwan Scholarship Test"
        user_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; }}
                .header {{ background-color: #0b1f3a; color: #ffffff; padding: 15px; border-radius: 6px 6px 0 0; font-size: 18px; font-weight: bold; }}
                .content {{ padding: 20px; background-color: #ffffff; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">VST Registration Successful!</div>
                <div class="content">
                    <p>Dear <strong>{vst_data.get('student_name')}</strong>,</p>
                    <p>Your registration for the <strong>Vidwan Scholarship Test (VST)</strong> has been confirmed!</p>
                    <p>Our team will contact you at <strong>{vst_data.get('phone')}</strong> with your admit card details, test syllabus, and exam schedule.</p>
                    <br>
                    <p>Good luck!</p>
                    <p><strong>Vidwan Classes Team</strong></p>
                </div>
            </div>
        </body>
        </html>
        """
        send_email(vst_data.get("email"), user_subject, user_html)
