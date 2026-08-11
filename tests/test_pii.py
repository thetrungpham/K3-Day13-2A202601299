from __future__ import annotations

import json
from pathlib import Path

from app import logging_config
from app.logging_config import configure_logging, get_logger
from app.pii import scrub_text


def test_scrub_email() -> None:
    out = scrub_text("Email me at student@vinuni.edu.vn")
    assert "student@" not in out
    assert "REDACTED_EMAIL" in out


def test_scrub_common_vietnamese_phone_formats() -> None:
    phone_numbers = (
        "0901234567",
        "090 123 4567",
        "090.123.4567",
        "090-123-4567",
        "+84 90 123 4567",
    )

    for phone_number in phone_numbers:
        out = scrub_text(f"Contact: {phone_number}")
        assert phone_number not in out
        assert "REDACTED_PHONE_VN" in out


def test_scrub_identity_and_payment_numbers() -> None:
    cases = (
        ("CCCD: 001204123456", "001204123456", "REDACTED_CCCD"),
        ("Card: 4111 1111 1111 1111", "4111 1111 1111 1111", "REDACTED_CREDIT_CARD"),
        ("Card: 4111-1111-1111-1111", "4111-1111-1111-1111", "REDACTED_CREDIT_CARD"),
        ("Passport: B1234567", "B1234567", "REDACTED_PASSPORT"),
    )

    for text, raw_value, marker in cases:
        out = scrub_text(text)
        assert raw_value not in out
        assert marker in out


def test_scrub_labeled_vietnamese_address() -> None:
    address = "Địa chỉ: 123 Nguyễn Trãi, Thanh Xuân, Hà Nội"

    out = scrub_text(f"Thông tin khách hàng; {address}")

    assert "123 Nguyễn Trãi" not in out
    assert "REDACTED_ADDRESS_VN" in out


def test_logging_processor_scrubs_pii_at_any_depth(
    monkeypatch, tmp_path: Path
) -> None:
    log_path = tmp_path / "logs.jsonl"
    monkeypatch.setattr(logging_config, "LOG_PATH", log_path)
    configure_logging()

    get_logger().info(
        "security_check",
        service="api",
        contact="student@vinuni.edu.vn",
        payload={
            "customers": [
                {
                    "phone": "090 123 4567",
                    "documents": ("001204123456", "B1234567"),
                }
            ]
        },
    )

    record = json.loads(log_path.read_text(encoding="utf-8").strip())
    serialized = json.dumps(record, ensure_ascii=False)

    assert "student@vinuni.edu.vn" not in serialized
    assert "090 123 4567" not in serialized
    assert "001204123456" not in serialized
    assert "B1234567" not in serialized
    assert record["contact"] == "[REDACTED_EMAIL]"
    assert "[REDACTED_PHONE_VN]" in serialized
    assert "[REDACTED_CCCD]" in serialized
    assert "[REDACTED_PASSPORT]" in serialized
