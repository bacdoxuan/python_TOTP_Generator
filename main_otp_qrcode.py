import pyotp
import time
import sys
import qrcode
from datetime import datetime, timezone
from main_upgrade import run_totp_app


def print_qr_code(secret: str, username: str, service: str):
    """
    Tạo và hiển thị mã QR trên Terminal sử dụng ký tự ASCII.
    """
    # 1. Tạo đường dẫn URI chuẩn cho TOTP (otpauth://...)
    # Đây là định dạng mà Google Authenticator/Authy yêu cầu
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name=service)

    # 2. Khởi tạo đối tượng QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    qr.add_data(uri)
    qr.make(fit=True)

    print("\n" + "=" * 60)
    print(f"{'SCAN THIS QR CODE':^60}")
    print("=" * 60)

    # 3. In QR ra màn hình console
    # invert=True thường cần thiết cho terminal nền đen (dark mode)
    # để biến các khối đen thành trắng và ngược lại, giúp camera nhận diện tốt hơn.
    qr.print_ascii(invert=True)

    print("=" * 60)
    print("Hãy mở ứng dụng Authenticator (Google/Microsoft) và quét mã trên.")
    input("Nhấn [Enter] sau khi đã quét xong để bắt đầu xem mã OTP...")


if __name__ == "__main__":
    # Secret Key ngẫu nhiên
    SECRET_KEY = pyotp.random_base32()
    USERNAME = "bacdoxuan@gmail.com"
    SERVICE = "OTP_AND_QRCODE"

    # Hiển thị QR Code trước
    print_qr_code(SECRET_KEY, USERNAME, SERVICE)


    # Hien thi OTP
    run_totp_app(SECRET_KEY, USERNAME, SERVICE)