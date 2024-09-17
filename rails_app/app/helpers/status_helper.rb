module StatusHelper
  # Determine the status as an integer
  def status_message_value(upload_id)
    status_record = Status.find_by(upload_id: upload_id)
    return 2 unless status_record # Default to 2 (warning) if no status record is found

    receiver_start = status_record.receiver_start
    receiver_preprocess = status_record.receiver_preprocess
    receiver_process = status_record.receiver_process

    if [ receiver_start, receiver_preprocess, receiver_process ].all? { |status| status == "complete" }
      0  # All steps are complete
    elsif [ receiver_start, receiver_preprocess, receiver_process ].any? { |status| status == "failed" }
      1  # At least one step has failed
    elsif [ receiver_start, receiver_preprocess, receiver_process ].any? { |status| status == "pending" }
      2  # Some steps are pending but none have failed
    else
      2  # Default to 2 (warning) status
    end
  end
end
