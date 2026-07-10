#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过 QQ 邮箱 SMTP 将 APK 作为附件发送到指定邮箱。
用法:
  python send_apk_email.py --apk yiqilai-stock-app-debug.apk \
      --sender 你的QQ号@qq.com --authcode 你的QQ邮箱授权码 \
      --to 860614153@qq.com
说明:
  - QQ 邮箱 SMTP 服务器 smtp.qq.com, SSL 端口 465
  - authcode 不是邮箱密码，而是 QQ 邮箱设置->账户->开启SMTP服务后生成的"授权码"
  - 若 sender 与 to 相同，即"发给自己"。
"""
import argparse
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--apk", required=True, help="APK 文件路径")
    p.add_argument("--sender", required=True, help="发件人 QQ 邮箱, 如 123456@qq.com")
    p.add_argument("--authcode", required=True, help="QQ 邮箱 SMTP 授权码")
    p.add_argument("--to", default="860614153@qq.com", help="收件人")
    p.add_argument("--smtp-host", default="smtp.qq.com")
    p.add_argument("--smtp-port", type=int, default=465)
    args = p.parse_args()

    if not os.path.isfile(args.apk):
        print(f"APK 文件不存在: {args.apk}")
        sys.exit(1)

    size_mb = os.path.getsize(args.apk) / 1024 / 1024
    print(f"准备发送: {args.apk} ({size_mb:.2f} MB) -> {args.to}")

    msg = MIMEMultipart()
    msg["From"] = args.sender
    msg["To"] = args.to
    msg["Subject"] = "易起来AI选股 App 调试版 APK"
    msg.attach(MIMEText(
        "您好，附件是《易起来AI选股》Android 调试版安装包 (app-debug.apk)。\n"
        "请在手机上用文件管理器打开安装；若提示'未知来源'，请允许浏览器/文件管理的安装权限。\n"
        "—— 由云端构建自动发送。", "plain", "utf-8"))

    with open(args.apk, "rb") as f:
        part = MIMEBase("application", "vnd.android.package-archive")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            "attachment",
            filename="yiqilai-stock-app-debug.apk",
        )
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL(args.smtp_host, args.smtp_port, timeout=60) as s:
            s.login(args.sender, args.authcode)
            s.sendmail(args.sender, [args.to], msg.as_string())
        print("邮件发送成功 ->", args.to)
    except smtplib.SMTPAuthenticationError as e:
        print("认证失败：授权码不正确或未开启 SMTP。错误:", e)
        sys.exit(2)
    except Exception as e:
        print("发送异常:", e)
        sys.exit(3)


if __name__ == "__main__":
    main()
