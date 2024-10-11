class UploadsController < ApplicationController
  rate_limit to: 20, within: 1.minute, only: [ :index ], with: -> { redirect_to root_path, alert: "Too many requests. Please try again" }

  before_action :set_upload, only: %i[show destroy]
  before_action :authenticate_user!, only: %i[show new create destroy]
  before_action :check_request_from_form, only: [ :search_items ]

  def index
    @uploads = Upload.order(created_at: :desc)
    @pagy, @uploads = pagy(@uploads)
  end

  def new
    @upload = Upload.new
  end

  def show
    @upload = Upload.find(params[:id])
  rescue ActiveRecord::RecordNotFound
    redirect_to root_path
  end

  def create
    @upload = current_user.uploads.build(upload_params)
    if @upload.save
      redirect_to upload_path(@upload), notice: "Upload was successfully created."
    else
      render :new
    end
  end

  def destroy
    @upload.destroy
    redirect_to uploads_url, notice: "Upload was successfully destroyed."
  end

  def search
  end

  def search_items
    @query=search_params["query"]
    @uploads = Upload.search_by_name(@query)
    .where(process_complete: true)
    .limit(10) || []
    @uploads = @uploads.sort_by(&:created_at).reverse
    respond_to do |format|
      format.turbo_stream do
          if @query.blank?
            render turbo_stream: turbo_stream.update("search_results", partial: "uploads/no_search")
          else
            render turbo_stream: turbo_stream.update("search_results", partial: "uploads/search_results", locals: { uploads: @uploads })
          end
        end
    end
  end

  private

  def check_request_from_form
    unless request.post? && params[:source] == "form"
      flash[:alert] = "Access denied"
      redirect_to root_path
    end
  end

  def set_upload
    @upload = Upload.find(params[:id])
  rescue ActiveRecord::RecordNotFound
    redirect_to root_path
  end

  def upload_params
    params.require(:upload).permit(:files)
  end

  def search_params
    params.permit([ :query, :authenticity_token, :source, :controller, :action ])
  end
end
