from datetime import datetime
import json
import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ALERT_BEFORE_DAYS = 5  # Báo trước 5 ngày


def send_telegram(message):
  """Gửi tin nhắn về Telegram cá nhân."""
  url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
  payload = {
      "chat_id": CHAT_ID,
      "text": message,
      "parse_mode": "HTML",
      "disable_web_page_preview": True,
  }
  try:
    res = requests.post(url, json=payload, timeout=10)
    res.raise_for_status()
  except Exception as e:
    print(f"Lỗi gửi Telegram: {e}")


def check_expirations():
  if not os.path.exists("domains.json"):
    print("Chưa tìm thấy file domains.json")
    return

  with open("domains.json", "r", encoding="utf-8") as f:
    items = json.load(f)

  today = datetime.now().date()
  print(f"Hôm nay là ngày: {today}")

  for item in items:
    try:
      end_date = datetime.strptime(item["end_date"].replace("/", "-"),, "%Y-%m-%d").date()
      days_left = (end_date - today).days

      # Điều kiện: Còn từ 0 đến 5 ngày là sẽ gửi cảnh báo
      if 0 <= days_left <= ALERT_BEFORE_DAYS:
        status_text = (
            f"Còn <b>{days_left} ngày</b>"
            if days_left > 0
            else "<b>HẾT HẠN HÔM NAY!</b>"
        )

        message = (
            f"⚠️ <b>CẢNH BÁO GIA HẠN LINK / DOMAIN</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🌐 <b>Site:</b> {item.get('site')}\n"
            f"💰 <b>Giá:</b> {item.get('price', 'N/A')}\n"
            f"⚓ <b>Anchor:</b> {item.get('anchor')}\n"
            f"🔗 <b>Link:</b> {item.get('link')}\n"
            f"⏳ <b>Tình trạng:</b> {status_text}\n"
            f"📅 <b>Hạn chót:</b> {item.get('end_date')}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👉 <i>Hãy liên hệ chủ site để gia hạn kịp thời!</i>"
        )

        send_telegram(message)
        print(f"Đã gửi cảnh báo cho: {item.get('site')} (Còn {days_left} ngày)")

      elif days_left < 0:
        print(f"{item.get('site')} đã quá hạn {-days_left} ngày.")
      else:
        print(f"{item.get('site')} còn {days_left} ngày, chưa đến mốc báo.")

    except Exception as err:
      print(f"Lỗi khi đọc mục {item}: {err}")


if __name__ == "__main__":
  check_expirations()
