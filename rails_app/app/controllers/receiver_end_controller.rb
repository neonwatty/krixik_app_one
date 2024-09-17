class ReceiverEndController < ApplicationController
  skip_before_action :verify_authenticity_token # For API requests
  before_action :authenticate_request

  def update
    payload = params.require(:receiver_end).permit(:bucket_name, :processed_key, :upload_id)
    upload = Upload.find_by(id: payload[:upload_id])

    if upload
      process_and_attach(
        processed_key: payload[:processed_key],
        bucket_name: payload[:bucket_name],
        upload: upload
      )
      render json: { status: "processed file updated" }
    else
      render json: { error: "Upload not found" }, status: :not_found
    end
  end

  private

  def authenticate_request
    auth_header = request.headers["Authorization"] || ""
    if auth_header.start_with?("Bearer ")
      token = auth_header.split(" ").last
      expected_token = Rails.application.config.lambda_api_key

      head :unauthorized unless ActiveSupport::SecurityUtils.secure_compare(token, expected_token)
    else
      head :unauthorized
    end
  end

  def process_and_attach(processed_key:, bucket_name:, upload:)
    s3 = Aws::S3::Client.new
    processed_data = s3.get_object(bucket: bucket_name, key: processed_key).body.read

    upload.files.attach(io: StringIO.new(processed_data), filename: File.basename(processed_key))
    upload.save

    s3.delete_object(bucket: bucket_name, key: processed_key)
  rescue Aws::S3::Errors::ServiceError => e
      Rails.logger.error "S3 Error: #{e.message}"
  end
end
