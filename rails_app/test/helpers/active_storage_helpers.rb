module ActiveStorageHelpers
  def attach_file_to(model, attachment_name, file_path)
    file = Rack::Test::UploadedFile.new(Rails.root.join(file_path), "image/jpeg")
    model.public_send("#{attachment_name}=").attach(io: file, filename: File.basename(file_path))
  end
end

class ActiveSupport::TestCase
  include ActiveStorageHelpers
end
