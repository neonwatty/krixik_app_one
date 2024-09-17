require "application_system_test_case"

class NewUploadTest < ApplicationSystemTestCase
  fixtures :all

  setup do
    @user = users(:one)
  end

  test "test_1: non-logged in user functionality - redirect to sign in" do
    visit new_upload_path
    assert_current_path new_user_session_path
  end

  test "test_2: logged in user functionality - details card" do
    sign_in(@user)
    visit new_upload_path
    assert_current_path new_upload_path
  end

  test "test_3: logged in user functionality - details card and new upload" do
    sign_in(@user)
    visit new_upload_path
    assert_current_path new_upload_path
    original_blob_count = ActiveStorage::Blob.count
    original_attachment_count = ActiveStorage::Attachment.count

    # Trigger JavaScript to reveal the hidden file input
    page.execute_script("
    var fileInput = document.getElementById('file_input_id');
    if (fileInput) {
      fileInput.style.display = 'block';  // Make the input visible
      fileInput.removeAttribute('disabled');  // Remove the disabled attribute
      }
    ")

    # Wait for the file input to be visible
    sleep 1

    # click on the file input
    attach_file("upload[files]", Rails.root + "test/fixtures/files/r_l_burnside.png")

    # submit the form
    click_button "Submit"

    # sleep for 5 seconds
    sleep 5

    # assert redirect to show page
    assert_current_path upload_path(Upload.last)

    # destroy the upload - click delete button
    click_button "Delete"

    # click ok on the confirm dialog
    page.driver.browser.switch_to.alert.accept

    # assert redirect to index page
    assert_current_path uploads_path
  end
end
