require "test_helper"

class UploadTest < ActiveSupport::TestCase
  # Load the fixtures
  fixtures :all

  test "check that upload has file attached" do
      files = uploads(:one).files
      assert files.attached?
  end

  test "should not save upload without files" do
    upload = Upload.new(user: users(:one))
    saved = upload.save
    assert_not saved, "Saved the upload without files"
  end

  test "should associate upload with user" do
    upload = Upload.new(user: users(:one))
    upload.files.attach(io: File.open(Rails.root.join("test/fixtures/files/mississippi_john_hurt.png")), filename: "mississippi_john_hurt.png")
    assert_equal users(:one), upload.user, "Upload is not associated with the correct user"
  end

  test "should have attached files and filename" do
    upload = Upload.new(user: users(:one))
    upload.files.attach(io: File.open(Rails.root.join("test/fixtures/files/mississippi_john_hurt.png")), filename: "mississippi_john_hurt.png")
    assert upload.files.attached?, "Upload should have files attached"
  end
end
