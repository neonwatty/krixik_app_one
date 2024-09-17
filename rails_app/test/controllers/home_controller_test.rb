require "test_helper"

class UploadsControllerTest < ActionDispatch::IntegrationTest
  def setup
    @upload = uploads(:one)
  end

  test "test_1: should get home" do
    get root_path
    assert_response :success
  end
end
