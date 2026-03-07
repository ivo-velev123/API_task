from conftest import BASE_URL

def test_can_see_coins(anonymous):
    assert anonymous.locator("h2").count() > 0

def test_cant_see_complete_button(anonymous):
    assert anonymous.locator("button:has-text('Mark complete')").count() == 0

def test_anonymous_user_gets_redirected_when_on_admin_page(anonymous):
    anonymous.goto(f"{BASE_URL}/admin")
    assert anonymous.url == f"{BASE_URL}/"

def test_anonymous_user_gets_redirected_when_on_logs_page(anonymous):
    anonymous.goto(f"{BASE_URL}/logs")
    assert anonymous.url == f"{BASE_URL}/"