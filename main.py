import pyotp
import time
import sys
import datetime


def display_totp_app(secret: str, username: str, service: str):
    """
    Function to display the TOTP app
    Args
        :param secret: secret code to generate totp
        :param username: username to generate totp
        :param service: service to generate totp
        :return:
    """
    totp = pyotp.TOTP(secret)

    print("=" * 60)
    print("TOTP App Generated")
    print("=" * 60)
    print("Username: " + username)
    print("Service: " + service)
    print("=" * 60)
    interval = 30

    try:
        now = datetime.datetime.now(datetime.timezone.utc)
        current_otp = totp.now()
        print("Time UTC : " + now.strftime("%Y-%m-%d %H:%M:%S"))
        print("OTP: " + str(current_otp))
        current_timestamp = int(time.time())
        time_step = current_timestamp // interval
        time_end = (time_step + 1) * interval
        print("Next OTP Time : " + time.strftime("%Y-%m-%d - %H:%M:%S", time.gmtime(time_end)))
        print("=" * 60)
        while True:
            current_timestamp = int(time.time())
            if current_timestamp >= time_end:
                time_end += interval
            count_down = time_end - current_timestamp
            if count_down == 30:
                now = datetime.datetime.now(datetime.timezone.utc)
                current_otp = totp.now()
                print("Time UTC : " + now.strftime("%Y-%m-%d %H:%M:%S"))
                print("OTP: " + str(current_otp))
                print("Next OTP Time : " + time.strftime("%Y-%m-%d - %H:%M:%S", time.gmtime(time_end)))
                print("=" * 60)
                sys.stdout.flush()
            # print(count_down)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    # Thông số đầu vào
    SECRET_KEY = pyotp.random_base32()
    print("SECRET_KEY: " + SECRET_KEY)
    USERNAME = "Nguyen Van An"
    SERVICE = "Google Account"

    # Chạy ứng dụng
    display_totp_app(SECRET_KEY, USERNAME, SERVICE)