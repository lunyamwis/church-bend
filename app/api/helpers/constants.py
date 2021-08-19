USER_REQUIRED_FIELD = ['first_name', 'last_name',
                       'username', 'email', 'password', 'phone_number']
EMPLOYEE_REQUIRED_FIELD = ['first_name', 'last_name', "email"]
INDIVIDUAL_CLIENT_REQUIRED_FIELD = ['first_name', 'last_name', 'gender']
CORPORATE_CLIENT_REQUIRED_FIELD = ['name', ]
RECEIPT_REQUIRED_FIELD = ["transaction_date",
                          "amount_figures", "amount_words", "payment_mode"]
CONTACT_PERSON_REQUIRED_FIELD = ['name', 'position', 'phone_number', 'email',
                                 'gender', 'service_line', ]
ADDITIONAL_PREMIUMS_REQUIRED_FIELDS = ['premium', 'minimum_amount']
INSURANCE_CO_REQUIRED_FIELD = ['name', 'email', 'mobile_number', 'contact_person',
                               'postal_address', ]
MOTOR_POLICY_REQUIRED_FIELD = ['policy_no', 'transaction_date', 'start_date', 'policy_commission_rate',
                               'end_date', 'vehicles', 'insurance_class', 'minimum_premium_amount',
                               'transaction_type', 'premium_type', 'vehicles', 'insurance_company']
PROFESSIONAL_INDEMNITY_REQUIRED_FIELD = ['policy_no', 'transaction_date', 'start_date',
                                         'end_date', 'sum_insured', 'premium_type',
                                         'total_premium', 'commission_rate', 'commission_amount', 'specialty_class',
                                         'transaction_type', 'premium_type', 'insurance_company']
INDIVIDUAL_MEDICAL_REQUIRED_FIELD = ['policy_no', 'transaction_date', 'start_date', 'debit_note_no',
                                     'end_date', 'premium_type', 'commission_rate', 'medical_insurance',
                                     'transaction_type', 'premium_type', 'insurance_company']
GROUP_MEDICAL_REQUIRED_FIELD = ['policy_no', 'transaction_date', 'start_date', 'debit_note_no',
                                'end_date', 'premium_type', 'commission_rate', 'medical_insurances',
                                'transaction_type', 'premium_type', 'insurance_company']
DOMESTIC_PACKAGE_REQUIRED_FIELD = ['policy_no', 'transaction_date', 'start_date', 'debit_note_no',
                                   'end_date', 'premium_type', 'commission_rate', 'package_details',
                                   'transaction_type', 'premium_type', 'insurance_company']
PERSONAL_ACC_REQUIRED_FIELD = ['policy_no', 'transaction_date', 'start_date', 'debit_note_no',
                               'end_date', 'premium_type', 'commission_rate', 'benefit_limits',
                               'transaction_type', 'premium_type', 'insurance_company']
PACKAGE_DETAILS_REQUIRED_FIELD = ['buildings', 'contents', 'all_risks',
                                  'work_man_injury', 'owner_liability', 'occupiers_liability']
FIRE_DETAILS_REQUIRED_FIELD = ['name', 'description', 'value']
FIRE_POLICY_REQUIRED_FIELD = ['policy_no', 'transaction_date', 'start_date', 'debit_note_no',
                              'end_date', 'premium_type', 'commission_rate', 'properties',
                              'transaction_type', 'premium_type', 'insurance_company']
WIBA_POLICY_REQUIRED_FIELD = ['policy_no', 'transaction_date', 'start_date', 'debit_note_no',
                              'end_date', 'premium_type', 'commission_rate', 'no_of_staff',
                              'transaction_type', 'premium_type', 'insurance_company',
                              'estimate_annual_earning']
TRAVEL_REQUIRED_FIELD = ['policy_no', 'transaction_date', 'start_date', 'debit_note_no',
                         'end_date', 'premium_type', 'commission_rate', 'travel_details',
                         'transaction_type', 'premium_type', 'insurance_company']
TRAVEL_DETAILS_REQUIRED_FIELD = ['option', 'passport_no', 'date_of_travel', 'next_of_kin',
                                 'countries_of_travel', 'modes_of_travel', 'reasons_of_travel']
SEND_MESSAGE_REQUIRED_FIELD = []
MEDICAL_INS_REQUIRED_FIELD = ['inpatient_limit', 'outpatient_limit', 'family_size']
MOTOR_VEHICLE_REQUIRED_FIELD = ['registration_no', 'make', 'model', 'body', 'color', 'year_of_manufacture',
                                'chassis_no', 'engine_no', 'seating_capacity', 'cc', 'tonnage']
SUCCESS_ACTION = "{} successfully"
MAIL_SUBJECT = 'Activate your account at {}'
SIGNUP_SUCCESS = "{0} account created successfully. {0} should check their email for confirmation"
AGENCY_SIGNUP_SUCCESS = "Agency and admin accounts created successfully. Please check the admin and agency emails for confirmaton"
USER_MAIL_BODY_MSG = "Thanks for choosing {}"
ADMIN_MAIL_BODY_MSG = "Thank you for registering {}. You are now the admin"
ACCOUNT_ACTIVATION_MSG = "To activate your account. Please click the lik below"
AGENCY_MAIL_BODY_MSG = "This is the insurance agency activation email "
GENDER_OPTIONS = {"M": "Male", "F": "Female", "O": "Prefer not to disclose"}
