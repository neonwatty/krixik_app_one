class HomeController < ApplicationController
  def index
  end

  # redirect all not found to root_path
  def not_found
    redirect_to root_path
  end
end
