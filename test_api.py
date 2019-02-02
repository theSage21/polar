import requests as R


def api(x):
    return "http://localhost:8000" + x


def test_listing_works():
    r = R.get(api("/api/ships"))
    assert r.status_code == 200, r.text
    assert r.json()["total"] == 3, r.json()


def test_position_listing_works():
    r = R.get(api("/api/ships"))
    assert r.status_code == 200, r.text
    assert r.json()["total"] == 3, r.json()
    imo = r.json()["ships"][0]["imo"]
    r = R.get(api(f"/api/positions/{imo}"))
    assert r.status_code == 200, r.text
