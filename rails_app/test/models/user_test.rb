require "test_helper"

class UserTest < ActiveSupport::TestCase
  test "should create a new user" do
    user = User.new(email: "user3@example.com", password: "password", password_confirmation: "password")
    assert user.save
  end

  test "should not create a new user with an existing email" do
    user = User.first
    new_user = User.new(email: user.email, password: "password", password_confirmation: "password")
    assert_not new_user.save
  end

  test "should not create a new user without email" do
    user = User.new(password: "password", password_confirmation: "password")
    assert_not user.save
  end

  test "should not create a new user without password" do
    user = User.new(email: "user3@example.com")
    assert_not user.save
  end

  test "should not create a new user with a password less than 8 characters" do
    user = User.new(email: "user3@example.com", password: "pass", password_confirmation: "pass")
    assert_not user.save
  end

  test "should not create a new user without password confirmation" do
    user = User.new(email: "user3@example.com", password: "password")
    assert_not user.save
  end

  test "users can have the same password" do
    user = User.new(email: "user3@example.com", password: "password", password_confirmation: "password")
    assert user.save
    user = User.new(email: "user4@example.com", password: "password", password_confirmation: "password")
    assert user.save
  end
end
