def test_signals_import(django_app, superuser):
    assert "Test Plugin" in django_app.get("/", user=superuser).text
