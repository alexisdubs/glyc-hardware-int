
def check_options(variables, options):
    invalid_vars = [var for var in variables if var not in options]
    if invalid_vars:
        raise Exception(f"The following options are not valid: {', '.join(invalid_vars)}")
