class Status < ApplicationRecord
  before_create :set_default_receiver_values

  belongs_to :upload


  private


  def set_default_receiver_values
    self.receiver_start = "pending"
    self.receiver_preprocess = "pending"
    self.receiver_process = "pending"
    self.receiver_end = "pending"
  end
end
