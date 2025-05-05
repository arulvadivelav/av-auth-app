from string import ascii_letters, digits
from random import choice
from datetime import datetime
import pytz
from auth_project.settings import EMAIL_AUTHOR


def mail_content(otp):
    MAIL_SUBJECT = f"Email Verification"
    MAIL_CONTENT = """
                    Dear user,

                    Thank you for using our services. To complete your verification process, please use the following One-Time Password (OTP):

                    Your OTP Code: {OTP}

                    Please note that this OTP is valid for 10 minutes and can only be used once. Do not share this code with anyone. 
                    If you did not request this OTP, please contact our support team immediately.

                    If you have any questions or need further assistance, feel free to reach out to our support team.

                    Best regards,
                    {EMAIL_AUTHOR}
                    """.format(
        OTP=otp, EMAIL_AUTHOR=EMAIL_AUTHOR
    )
    return MAIL_SUBJECT, MAIL_CONTENT


def generate_otp(otp_length):
    try:
        # To generate a random string
        str_list = [choice(ascii_letters + digits) for _ in range(otp_length)]
        OTP = "".join(str_list)
        return True, "OTP generated.", OTP
    except:
        return False, "Failed to generate OTP.", ""


def convert_time(datetime_str, to_timezone="UTC"):
    try:
        # Define the UTC and IST timezones
        utc = pytz.UTC
        ist = pytz.timezone("Asia/Kolkata")

        # Parse the datetime string into a datetime object and set it to UTC timezone
        utc_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=utc
        )

        # Convert the UTC time to the specified timezone
        if to_timezone.upper() == "IST":
            target_time = utc_time.astimezone(ist)
        else:
            target_time = utc_time

        # Format the datetime object into a string
        formatted_time = target_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
        return True, target_time, formatted_time
    except:
        return False, "", ""
