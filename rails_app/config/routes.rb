Rails.application.routes.draw do
  devise_for :users, controllers: {
    confirmations: "users/confirmations",
    sessions: "users/sessions",
    registrations: "users/registrations"
    }
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Reveal health status on /up that returns 200 if the app boots with no exceptions, otherwise 500.
  # Can be used by load balancers and uptime monitors to verify that the app is live.
  get "up" => "rails/health#show", as: :rails_health_check

  # Render dynamic PWA files from app/views/pwa/*
  get "service-worker" => "rails/pwa#service_worker", as: :pwa_service_worker
  get "manifest" => "rails/pwa#manifest", as: :pwa_manifest

  # receiver routes
  post "receiver_end/update", to: "receiver_end#update"
  post "receiver_status/update", to: "receiver_status#update"
  patch "receiver_status/update", to: "receiver_status#update"
  post "receiver_outputs/update", to: "receiver_outputs#update"
  patch "receiver_outputs/update", to: "receiver_outputs#update"


  # Define root path
  root "home#index"

  # Route for 'home' page
  get "home", to: "home#index", as: "home"

  # Search route
  get "search", to: "uploads#search"

  # Resources for 'uploads' with custom collection route
  resources :uploads, except: [ :update, :edit ] do
    collection do
      post "search_items"
    end
  end

  # Catch-all route for non-existent pages, to be used unless assets are being compiled
  match "*path", via: :all, to: "application#not_found", constraints: lambda { |req|
    req.path.exclude? "rails/active_storage"
}
end
