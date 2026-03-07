from conftest import BASE_URL

def test_login(user):
    assert user.url == f"{BASE_URL}/"

def test_can_see_complete_button(user):
    assert user.locator("button:has-text('Mark complete')").count() > 0

def test_user_can_toggle_coin(user):
    user.locator("button:has-text('Mark complete')").first.click()
    assert user.locator("button:has-text('Mark incomplete')").count() > 0

def test_user_cant_access_admin(user):
    user.goto(f"{BASE_URL}/admin")
    assert user.url == f"{BASE_URL}/"

def test_user_cant_access_logs(user):
    user.goto(f"{BASE_URL}/logs")
    assert user.url == f"{BASE_URL}/"

def test_user_can_log_out(user):
    user.click("button:has-text('Logout')")
    assert user.url == f"{BASE_URL}/login"