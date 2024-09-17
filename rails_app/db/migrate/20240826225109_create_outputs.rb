class CreateOutputs < ActiveRecord::Migration[7.2]
  def change
    create_table :outputs do |t|
      t.belongs_to :upload, null: false, foreign_key: true
      t.string :result

      t.timestamps
    end
  end
end
