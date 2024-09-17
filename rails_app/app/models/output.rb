class Output < ApplicationRecord
  before_create :set_result_default

  belongs_to :upload

  private
  def set_result_default
    self.result = "not yet available"
  end
end
