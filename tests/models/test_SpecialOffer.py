import pytest

from datetime import datetime

@pytest.mark.usefixtures("db_session")
def test_special_offer_creation(offer):
    """Тестирование создания специального предложения."""
    assert offer.offer_id is not None
    assert offer.offer_title == "Sample Discount"
    assert offer.discount_size == 20.0
    assert offer.end_date == datetime.strptime("2024-12-31", "%Y-%m-%d").date()
