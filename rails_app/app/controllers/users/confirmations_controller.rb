class Users::ConfirmationsController < Devise::ConfirmationsController
  rate_limit to: 10, within: 5.minutes, only: [ :create ], with: -> { redirect_to root_path, alert: "Too many confirmation attempts. Please try again" }

  private
  def after_confirmation_path_for(resource_name, resource)
    sign_in(resource) # In case you want to sign in the user
    root_path
  end
end
