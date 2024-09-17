require "test_helper"

class UploadsControllerTest < ActionDispatch::IntegrationTest
  def setup
    @upload = uploads(:one)
    @valid_query_params = { query: "test query", source: "form" }
    @invalid_source_query_params = { query: "test query", source: "not-form" }
    @invalid_nosource_query_params = { query: "test query" }
  end

  test "test_1: index - uploads_controller_noauth_test" do
    get uploads_path
    assert_response :success
  end

  test "test_2: new - uploads_controller_noauth_test" do
    get new_upload_path
    assert_redirected_to new_user_session_path
  end

  test "test_3: show - uploads_controller_noauth_test" do
    get upload_path(@upload)
    assert_redirected_to new_user_session_path
  end

  test "test_4: create - uploads_controller_noauth_test" do
    post uploads_path
    assert_redirected_to new_user_session_path
  end

  test "test_5: destroy - uploads_controller_noauth_test" do
    delete upload_path(@upload)
    assert_redirected_to new_user_session_path
  end

  test "test_6: search - uploads_controller_noauth_test" do
    get search_path
    assert_response :success
  end

  test "test_7: search_items success (:source==form provided) - uploads_controller_noauth_test" do
    post search_items_uploads_path, params: @valid_query_params, as: :turbo_stream
    assert_response :success
    assert_match /<turbo-stream/, @response.body
  end

  test "test_8: search_items failure (:source==not-form provided) - uploads_controller_noauth_test" do
    post search_items_uploads_path, params: @invalid_source_query_params, as: :turbo_stream
    assert_redirected_to root_path
  end

  test "test_9: search_items failure (:source not provided) - uploads_controller_noauth_test" do
    post search_items_uploads_path, params: @invalid_nosource_query_params, as: :turbo_stream
    assert_redirected_to root_path
  end
end
