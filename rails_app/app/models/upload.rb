class Upload < ApplicationRecord
  include PgSearch::Model
  pg_search_scope :search_by_name, against: :filename, using: { tsearch: { prefix: true } }

  belongs_to :user

  has_many_attached :files do |attachable|
    attachable.variant :thumb, resize_to_limit: [ 100, 100 ], preprocessed: true
  end

  has_one :status, dependent: :destroy
  has_one :output, dependent: :destroy
  before_save :set_filename

  after_create :create_status
  after_create :create_output

  validates :files, presence: true
  after_commit :check_and_invoke_lambda, on: :create

  private

  def set_filename
    if files.attached? && !files_attached
      if files.count == 1
        self.filename = files.first.filename.to_s
      end
    end
  end

  def check_and_invoke_lambda
    if files.attached? && !files_attached
      # Check if this is the first file being attached
      if files.count == 1
        file_key = files.first.key # Get the key of the first attached file
        # Pass upload_id and user_id to the LambdaInvoker
        ReceiverStart.new.invoke_function(file_key, id, user_id)
        update(files_attached: true)
      end
    end
  end
  def create_status
    Status.create(upload: self)
  end
  def create_output
    Output.create(upload: self)
  end
end
