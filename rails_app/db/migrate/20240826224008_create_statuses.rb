class CreateStatuses < ActiveRecord::Migration[7.2]
  def change
    create_table :statuses do |t|
      t.belongs_to :upload, null: false, foreign_key: true
      t.string :receiver_start
      t.string :receiver_preprocess
      t.string :receiver_process
      t.string :receiver_end

      t.timestamps
    end
  end
end
