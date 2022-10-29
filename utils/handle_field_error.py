def handle_field_error(validation_error):
  errors = validation_error.__dict__.get('errors')
  err_dict = {}
  for error in errors:
    err_dict[error] = str(errors[error])
  return err_dict