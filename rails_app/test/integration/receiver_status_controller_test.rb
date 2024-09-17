require "test_helper"

class ReceiverStatusControllerTest < ActionDispatch::IntegrationTest
  test "test_1: should update status with valid data" do
    @upload = uploads(:one)
    payload = {
      receiver_status: {
        lambda: "receiver_start",
        user_id: 1,
        upload_id: @upload.id,
        status: "complete"
      }
    }

    # Send a PATCH request to the receiver_status controller
    patch "/receiver_status/update", params: payload.to_json, headers: {
      'Content-Type': "application/json",
      'Authorization': "Bearer #{ENV['LAMBDA_API_KEY_TEST']}"
    }

    # Assert the response status
    assert_response :ok

    # Assert the response message
    assert_equal JSON.parse(response.body)["message"], "Status updated successfully"

    # Assert the status record is updated
    assert_equal Status.find(@upload.id).receiver_start, "complete"
  end

  test "test_2: should return error for invalid status" do
    @upload = uploads(:one)
    payload = {
      receiver_status: {
        lambda: "receiver_start",
        user_id: 1,
        upload_id: @upload.id,
        status: "invalid_status"
      }
    }

    # Send a PATCH request to the receiver_status controller
    patch "/receiver_status/update", params: payload.to_json, headers: {
      'Content-Type': "application/json",
      'Authorization': "Bearer #{ENV['LAMBDA_API_KEY_TEST']}"
    }

    assert_response :unprocessable_entity
    assert_equal JSON.parse(response.body)["error"], "Invalid status"
  end

  test "should return error for invalid lambda function" do
    @upload = uploads(:one)
    payload = {
      receiver_status: {
        lambda: "invalid_lambda",
        user_id: 1,
        upload_id: @upload.id,
        status: "complete"
      }
    }

    # Send a PATCH request to the receiver_status controller
    patch "/receiver_status/update", params: payload.to_json, headers: {
      'Content-Type': "application/json",
      'Authorization': "Bearer #{ENV['LAMBDA_API_KEY_TEST']}"
    }

    assert_response :unprocessable_entity
    assert_equal JSON.parse(response.body)["error"], "Invalid lambda function"
  end

  test "should return error when upload_id not found" do
    payload = {
      receiver_status: {
        lambda: "receiver_start",
        user_id: 1,
        upload_id: 0,
        status: "complete"
      }
    }

    # Send a PATCH request to the receiver_status controller
    patch "/receiver_status/update", params: payload.to_json, headers: {
      'Content-Type': "application/json",
      'Authorization': "Bearer #{ENV['LAMBDA_API_KEY_TEST']}"
    }

    assert_response :not_found
    assert_equal JSON.parse(response.body)["error"], "Status record not found"
  end

  test "should return unauthorized for missing API key" do
    @upload = uploads(:one)
    payload = {
      receiver_status: {
        lambda: "receiver_start",
        user_id: 1,
        upload_id: @upload.id,
        status: "complete"
      }
    }

    # Send a PATCH request to the receiver_status controller
    patch "/receiver_status/update", params: payload.to_json, headers: {
      'Content-Type': "application/json"
    }

    assert_response :unauthorized
  end
end
