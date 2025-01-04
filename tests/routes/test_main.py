def test_index_categories(client, db_session, category):
    """Тест получения всех категорий для слайдера."""
    response = client.get("api/categories_all")
    assert response.status_code == 200
    data = response.get_json()

    assert data["success"] is True
    assert "categories" in data
    assert len(data["categories"]) == 1
    assert data["categories"][0]["category_title"] == category.category_title
    assert data["categories"][0]["category_description"] == category.category_description

def test_index_countries(client, db_session, country):
    """Тест получения всех стран для выпадающего списка."""
    response = client.get("api/countries_all")
    assert response.status_code == 200
    data = response.get_json()

    assert data["success"] is True
    assert "countries" in data
    assert len(data["countries"]) == 1
    assert data["countries"][0]["country_name"] == country.country_name
    assert data["countries"][0]["country_description"] == country.country_description

def test_index_categories_no_data(client, db_session):
    """Тест получения категорий, когда их нет в базе данных."""
    response = client.get("api/categories_all")
    assert response.status_code == 200
    data = response.get_json()

    assert data["success"] is True
    assert "categories" in data
    assert len(data["categories"]) == 0

def test_index_countries_no_data(client, db_session):
    """Тест получения стран, когда их нет в базе данных."""
    response = client.get("api/countries_all")
    assert response.status_code == 200
    data = response.get_json()

    assert data["success"] is True
    assert "countries" in data
    assert len(data["countries"]) == 0
