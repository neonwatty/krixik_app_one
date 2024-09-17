Aws.config.update({
   credentials: Aws::Credentials.new(ENV["RAILS_AWS_ACCESS_KEY_ID"],  ENV["RAILS_AWS_SECRET_ACCESS_KEY"]),
   region: ENV["AWS_REGION"]
})
