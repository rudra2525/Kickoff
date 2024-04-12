from nicegui import ui
from Dbconnector import Dbfunction

class AwsDetailsForm:
    def __init__(self):
        self.db = Dbfunction()
        self.form_data = {}
        self.initialize_fields()

        # Elements references will be stored here after setup
        self.field_elements = {}

        self.new_account_fields = [
            'outlook_distribution_list',
            'dl_members',
            'account_admin',
            'cloud_health_users',
            'cost_center',
            'primary_contact',
            'secondary_contact',
            'technical_contact',
            'client_ID',
            'environment_type',
            'gm_approval',

            # ...add all other keys for new account fields
        ]

        self.subscription_fields = [
            'aws_account',
            'aws_region',
            'os_type',
            'instance_type',
            # ...add all other keys for subscription fields
        ]

    def initialize_fields(self):
        # Initialize all fields to None
        self.outlook_distribution_list = None
        self.account_type = None
        self.dl_members = None
        self.account_admin = None
        self.cloud_health_users = None
        self.cost_center = None
        self.primary_contact = None
        self.secondary_contact = None
        self.technical_contact = None
        self.client_ID = None
        self.environment_type = None
        self.gm_approval = None
        # Initialize additional fields for subscription
        self.aws_account = None
        self.aws_region = None
        self.os_type = None
        self.instance_type = None

    # Mock function to retrieve stored data for Subscriptions

    def update_form_data(self, event=None):
        # Implementation to update form_data based on the input fields
        self.form_data['Outlook Distribution list'] = self.outlook_distribution_list.value
        self.form_data['DL Members'] = self.dl_members.value
        self.form_data['Account Admins'] = self.account_admin.value
        self.form_data['Cloud Health Users'] = self.cloud_health_users.value
        self.form_data['Accounting Cost Center'] = self.cost_center.value
        self.form_data['Primary contact'] = self.primary_contact.value
        self.form_data['Secondary contact'] = self.secondary_contact.value
        self.form_data['Technical contact'] = self.technical_contact.value
        self.form_data['Four Digit Client ID'] = self.client_ID.value
        self.form_data['Environment Type'] = self.environment_type.value
        self.form_data['GM Approval'] = self.gm_approval.value

    def update_aws_details(self, event):
        # Update form_data with the values from inputs
        self.form_data['aws_details'] = {  # Collect all AWS details
            'account_type': self.account_type.value,
            # ... [other fields as needed]
        }

    def on_account_type_change(self, event):
        account_type = event.value
        if account_type == 'New Account':
            for field_key in self.new_account_fields:
                self.field_elements[field_key].visible = True  # Show field
            for field_key in self.subscription_fields:
                self.field_elements[field_key].visible = False  # Hide field
        elif account_type == 'Subscriptions':
            for field_key in self.new_account_fields:
                self.field_elements[field_key].visible = False  # Hide field
            for field_key in self.subscription_fields:
                self.field_elements[field_key].visible = True  # Show field

    def show_new_account_fields(self):
        # Show fields related to 'New Account'
        self.field_elements['outlook_distribution_list'].show()
        self.field_elements['dl_members'].show()
        self.field_elements['account_admin'].show()
        self.field_elements['cloud_health_users'].show()
        self.field_elements['cost_center'].show()
        self.field_elements['primary_contact'].show()
        self.field_elements['secondary_contact'].show()
        self.field_elements['technical_contact'].show()
        self.field_elements['client_ID'].show()
        self.field_elements['environment_type'].show()
        self.field_elements['gm_approval'].show()
        # ... show all other fields related to new account

    def show_subscription_fields(self):
        # Show fields related to 'Subscriptions'
        self.field_elements['aws_account'].show()
        self.field_elements['aws_region'].show()
        self.field_elements['os_type'].show()
        self.field_elements['instance_type'].show()
        # ... show all other fields related to subscription



    def setup_aws_details_tab(self):
        self.account_type_switch = ui.switch('New Account', value=True, on_change=self.on_account_type_change)
        self.field_elements['aws_account'] = ui.select(label='AWS Account', options=[]).classes('w-60')
        self.field_elements['aws_account'].visible = False

        self.setup_aws_region_dropdown()
        self.setup_os_type_dropdown()

        # Update visibility based on initial switch state
        self.update_dropdown_visibility()


        # Setup all input fields and store their references
        self.field_elements['outlook_distribution_list'] = ui.input(label='Outlook Distribution list').classes('pl-12 w-full')
        self.field_elements['dl_members'] = ui.textarea(label='DL Members')
        self.field_elements['account_admin'] = ui.textarea(label='Account Admins')
        self.field_elements['cloud_health_users'] = ui.textarea(label='Cloud Health Users')
        self.field_elements['cost_center'] = ui.textarea(label='Accounting Cost Center')
        self.field_elements['primary_contact'] = ui.textarea(label='Primary contact')
        self.field_elements['secondary_contact'] = ui.textarea(label='Secondary contact')
        self.field_elements['technical_contact'] = ui.textarea(label='Technical contact')
        self.field_elements['client_ID'] = ui.textarea(label='Four Digit Client ID')
        self.field_elements['environment_type'] = ui.textarea(label='Environment Type')
        self.field_elements['gm_approval'] = ui.textarea(label='GM Approval')
        # ... setup and hide all other fields

        # Additional fields for subscriptions
        #self.field_elements['aws_account'] = ui.input(label='AWS Account')
        #self.field_elements['aws_region'] = ui.input(label='AWS Region')
        #self.field_elements['os_type'] = ui.input(label='OS Type')
        self.field_elements['instance_type'] = ui.input(label='Instance Type')



        for element in self.field_elements.values():
            if hasattr(element, 'visible'):
                element.visible = False

        self.update_fields_visibility(self.account_type_switch.value)

        ui.button('Save Details', on_click=self.update_aws_details)

    def setup_aws_region_dropdown(self):
        aws_regions = self.db.query_awsRegion()
        if isinstance(aws_regions, dict):
            # Convert the dictionary to a list of tuples and sort by region name
            region_options = sorted(aws_regions.items(), key=lambda item: item[1])
            self.field_elements['aws_region'] = ui.select(label='AWS Region', options=region_options).classes('w-60')
        else:
            print("Unexpected data structure for AWS regions")

    def setup_aws_account_dropdown(self, client_code):
        aws_accounts = self.db.query_awsAcc(client_code)
        awsAccName = sorted({value for value in aws_accounts.values()})
        account_options = [(acc_num, f"{acc_num} - {desc}") for acc_num, desc in aws_accounts.items()]

        if 'aws_account' in self.field_elements:
            # If it exists, just update its options
            self.field_elements['aws_account'].options = account_options
        else:
            # If it doesn't exist, create the dropdown and add it to field_elements
            self.field_elements['aws_account'] = ui.select(label='AWS Account', options=awsAccName).classes('w-60')

            # Set the visibility based on the account type
        self.field_elements['aws_account'].visible = not self.account_type_switch.value

    def setup_os_type_dropdown(self):
        os_types = self.db.query_os_type()
        os_type_options = [(os_type['OS_TYPE_NAME']) for os_type in os_types]

        if 'os_type' in self.field_elements:
            # If the dropdown exists, update its options using OS type names only
            self.field_elements['os_type'].options = os_type_options
        else:
            # If the dropdown doesn't exist, create it using OS type names only
            self.field_elements['os_type'] = ui.select(label='OS Type', options=os_type_options).classes('w-60')

        # Set the visibility based on the account type
        self.field_elements['os_type'].visible = not self.account_type_switch.value

    def on_account_type_change(self, event):
        is_new_account = self.account_type_switch.value
        self.update_fields_visibility(is_new_account)

        # Update the dropdown visibility as well, if needed
        self.update_dropdown_visibility()

    def update_dropdown_visibility(self):
        # The switch is 'off' when the value is False, hence dropdowns should be visible
        should_be_visible = not self.account_type_switch.value

        # Set the visibility of the dropdowns based on the switch state

        if 'aws_account' in self.field_elements:
            # Make sure the 'os_type' dropdown is visible if the switch is off
            self.field_elements['aws_account'].visible = should_be_visible

        if 'aws_region' in self.field_elements:
            # Make sure the 'os_type' dropdown is visible if the switch is off
            self.field_elements['aws_region'].visible = should_be_visible

        if 'os_type' in self.field_elements:
            # Make sure the 'os_type' dropdown is visible if the switch is off
            self.field_elements['os_type'].visible = should_be_visible


    def update_fields_visibility(self, is_new_account):
        # Hide or show fields based on whether it's a new account or subscription
        for field_key in self.new_account_fields:
            if field_key in self.field_elements:
                self.field_elements[field_key].visible = is_new_account

        for field_key in self.subscription_fields:
            if field_key in self.field_elements:
                self.field_elements[field_key].visible = not is_new_account

        # Update the visibility of aws_account and aws_region dropdowns
        self.update_dropdown_visibility()

