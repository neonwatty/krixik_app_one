require "application_system_test_case"

class AllUploadsTest < ApplicationSystemTestCase
  fixtures :all

  setup do
    @user = users(:one)
    @upload = uploads(:two)
  end

  test "test_1: non-logged in user functionality - all uploads" do
    visit uploads_path
    assert_selector "#navbar"
    assert_selector "#all-uploads-results"
  end

  test "test_2: check that upload has files.attached" do
    assert @upload.files.attached?, "upload should have file attached via fixture"
  end

  test "test_3: check that details from upload are accessible if not logged in" do
    visit uploads_path
    assert_selector "#navbar"
    assert_selector "#all-uploads-results"
    within "upload_results" do
      click_on "Details"
    end
    assert_current_path new_user_session_path
  end


  test "test_4: check that details from upload not accessible if logged in" do
    # visit
    visit uploads_path
    assert_selector "#navbar"
    assert_selector "#all-uploads-results"

    # sign in user and examine details card
    sign_in(@user)
    within "upload_results" do
      click_on "Details"
    end

    # details card
    assert_current_path upload_path(@upload)
  end
end
