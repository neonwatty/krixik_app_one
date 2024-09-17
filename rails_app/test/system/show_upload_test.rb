require "application_system_test_case"

class ShowUploadTest < ApplicationSystemTestCase
  fixtures :all

  setup do
    @user = users(:one)
    @upload = uploads(:two)
  end

  test "test_1: non-logged in user functionality - redirect to sign in" do
    visit upload_path(@upload)
    assert_current_path new_user_session_path
  end

  test "test_1: logged in user functionality - details card" do
    sign_in(@user)
    visit upload_path(@upload)
    assert_current_path upload_path(@upload)
  end
end
