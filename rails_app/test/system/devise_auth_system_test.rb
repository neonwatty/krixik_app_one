require "application_system_test_case"

class DeviseAuthSystemTest < ApplicationSystemTestCase
  fixtures :all

  def setup
    @user = users(:one)
  end

  test "test_1: sign in existing user (from seed)" do
    # set to homepage and see if 'Log in' link is present
    visit root_path
    assert_link "Log in", href: new_user_session_path

    # visit login page and fill in form
    visit new_user_session_path
    assert_selector "#new_user"
    fill_in "user_email", with: @user.email
    fill_in "user_password", with: "password123"
    click_on "new-session-login-btn"
    assert_current_path root_path

    # confirm login - 'Log in' link should not be present
    assert_no_link "Log in", href: new_user_session_path

    # log out and confirm 'Log in' link is present
    click_on "Log out"
    assert_current_path root_path
    assert_link "Log in", href: new_user_session_path
  end

  test "test_2: sign up" do
    # set to homepage and see if 'Log in' link is present
    visit root_path
    assert_link "Log in", href: new_user_session_path
    assert_link "Sign up", href: new_user_registration_path

    # visit signup page and fill in form
    visit new_user_registration_path
    fill_in "new-user-email-field", with: "dummy@dummy.com"
    fill_in "new-user-password-field", with: "password"
    fill_in "new-user-password-confirm-field", with: "password"
    click_on "signup-registration-btn"
    assert_current_path root_path
  end

  test "test_4: edit user profile" do
    # login
    visit new_user_session_path
    fill_in "user_email", with: @user.email
    fill_in "user_password", with: "password123"
    click_on "new-session-login-btn"
    assert_current_path root_path

    # visit edit page
    visit edit_user_registration_path
    assert_current_path edit_user_registration_path

    # fill in field based on id
    fill_in "edit-profile-email", with: "blah@blah.com"
    fill_in "edit-profile-password-new", with: "password456"
    fill_in "edit-profile-password-new-confirm", with: "password456"
    fill_in "edit-profile-password-current", with: "password123"
    click_on "update-profile-btn"
    assert_current_path root_path
end

  test "test_5: password reminder" do
    # visit login page and click on 'Forgot your password?'
    visit new_user_session_path
    click_on "Forgot your password?"
    assert_current_path new_user_password_path

    # fill in email and click on 'Send me reset password instructions'
    fill_in "user_email", with: @user.email
    click_on "send-reset-password-btn"
    assert_current_path new_user_session_path
  end
end
