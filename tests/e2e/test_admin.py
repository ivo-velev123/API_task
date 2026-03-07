from conftest import BASE_URL

def test_login(admin):
    assert admin.url == f"{BASE_URL}/"

def test_can_see_admin_link(admin):
    assert admin.locator("a:has-text('Admin')").count() > 0

def test_can_access_admin(admin):
    admin.goto(f"{BASE_URL}/admin")
    assert admin.url == f"{BASE_URL}/admin"

def test_can_create_coin(admin):
    admin.goto(f"{BASE_URL}/admin")
    admin.fill("input[name='coin_name']", "Test Coin")
    admin.clilck("button:has-text('Add coin')")
    assert admin.locator("td:has-text('Test Coin')").count() > 0

def test_can_delete_coin(admin):
    admin.goto(f"{BASE_URL}/admin")
    admin.locator("button:has-text('Delete')").first.click()
    assert admin.url == f"{BASE_URL}/admin"

def test_can_access_logs(admin):
    admin.goto(f"{BASE_URL}/logs")
    assert admin.url == f"{BASE_URL}/logs"

def test_can_logout(admin):
    admin.click("button:has-text('Logout')")
    assert admin.url == f"{BASE_URL}/login"