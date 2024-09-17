require "test_helper"

class LambdaOutputsControllerTest < ActionDispatch::IntegrationTest
  fixtures :all

  test "should update outputs with valid data" do
    @upload = uploads(:one)
    payload = {
      receiver_outputs: {
        upload_id: @upload.id,
        result: "this is a result"
      }
    }

    # Send a PATCH request to the receiver_outputs controller
    patch "/receiver_outputs/update", params: payload.to_json, headers: {
      'Content-Type': "application/json",
      'Authorization': "Bearer #{ENV['LAMBDA_API_KEY_TEST']}"
    }

    # Assert the response status
    assert_response :ok

    # Assert the response message
    assert_equal JSON.parse(response.body)["message"], "Output updated successfully"

    # Assert the status record is updated
    assert_equal Output.find(@upload.id).result, "this is a result"
  end

  test "should return error when upload_id not found" do
    payload = {
      receiver_outputs: {
        upload_id: 0,
        result: "this is a result"
      }
    }
    # Send a PATCH request to the receiver_outputs controller
    patch "/receiver_outputs/update", params: payload.to_json, headers: {
      'Content-Type': "application/json",
      'Authorization': "Bearer #{ENV['LAMBDA_API_KEY_TEST']}"
    }

    assert_response :not_found
    assert_equal JSON.parse(response.body)["error"], "Output record not found"
  end

  test "should return unauthorized for missing API key" do
    @upload = uploads(:one)
    payload = {
      receiver_outputs: {
        upload_id: @upload.id,
        result: "this is a result"
      }
    }

    # Send a PATCH request to the receiver_outputs controller
    patch "/receiver_outputs/update", params: payload.to_json, headers: {
      'Content-Type': "application/json"
    }

    assert_response :unauthorized
  end
end
