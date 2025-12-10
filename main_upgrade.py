import pyotp
import time
import sys
from datetime import datetime, timezone


def display_dashboard(secret: str, username: str, service: str):
    """
    Hiển thị thông tin header của ứng dụng.
    """
    print("=" * 75)
    print(f"{'TOTP AUTHENTICATOR':^60}")  # Căn giữa text
    print("=" * 75)
    print(f"User    : {username}")
    print(f"Service : {service}")
    # Chỉ hiện một phần secret để bảo mật nếu cần, hoặc hiện hết khi debug
    print(f"Secret  : {secret}")
    print("=" * 75)
    print(f"{'OTP CODE':^15} | {'REMAINING':^36} | {'TIME (UTC)':}")
    print("-" * 75)


def run_totp_app(secret: str, username: str, service: str):
    """
    Hàm chính để chạy vòng lặp hiển thị TOTP.

    Args:
        secret (str): Mã bí mật Base32.
        username (str): Tên người dùng.
        service (str): Tên dịch vụ.
    """
    # Khởi tạo đối tượng TOTP
    try:
        totp = pyotp.TOTP(secret)
        interval = totp.interval  # Mặc định là 30s
    except Exception as e:
        print(f"Lỗi khởi tạo TOTP: {e}")
        return

    display_dashboard(secret, username, service)

    try:
        while True:
            # Lấy thời gian hiện tại
            now_utc = datetime.now(timezone.utc)
            # current_timestamp = time.time()

            # Tạo OTP hiện tại
            current_otp = totp.now()

            # Tính toán thời gian còn lại của chu kỳ hiện tại
            # time_remaining = interval - (current_timestamp % interval)
            time_remaining = int(totp.interval - (datetime.now().timestamp() % totp.interval))

            # Tạo thanh hiển thị đếm ngược (Progress Bar)
            # Ví dụ: [##########] (đầy) -> [#####     ] (còn một nửa)
            bar_length = 30
            filled_length = int(bar_length * time_remaining // interval)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)

            # Định dạng màu sắc (nếu terminal hỗ trợ) hoặc format chuỗi
            # Sử dụng \r để đưa con trỏ về đầu dòng, giúp update tại chỗ thay vì in dòng mới
            output = (
                f"\r {current_otp:^13} | "
                f" {time_remaining:02d}s [{bar}] | "
                f" {now_utc.strftime('%H:%M:%S')}"
            )

            sys.stdout.write(output)
            sys.stdout.flush()

            # Ngủ 1 giây trước khi cập nhật tiếp
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Đã dừng ứng dụng. Tạm biệt! 👋")
        sys.exit(0)


if __name__ == "__main__":
    # Cấu hình đầu vào
    # Lưu ý: Trong thực tế, Secret Key nên được load từ biến môi trường hoặc nơi lưu trữ an toàn
    SAMPLE_SECRET = pyotp.random_base32()
    SAMPLE_USER = "Nguyen Van An"
    SAMPLE_SERVICE = "Google Account"

    run_totp_app(SAMPLE_SECRET, SAMPLE_USER, SAMPLE_SERVICE)