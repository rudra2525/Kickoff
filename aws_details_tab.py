from nicegui import ui

# Assuming form_data and other necessary imports or global variables are managed appropriately
#account_type = None
class AwsDetailsForm:
    def __init__(self):
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
        # Setup the account type selector
        self.account_type_switch = ui.switch(
            'New Account',
            value=True,  # Assuming True means 'New Account', False means 'Subscription'
            on_change=self.on_account_type_change
        )



        # Setup all input fields and store their references
        self.field_elements['outlook_distribution_list'] = ui.input(label='Outlook Distribution list')
        self.field_elements['dl_members'] = ui.textarea(label='DL Members')
        self.field_elements['account_admin']= ui.textarea(label='Account Admins')
        self.field_elements['cloud_health_users']= ui.textarea(label='Cloud Health Users')
        self.field_elements['cost_center']= ui.textarea(label='Accounting Cost Center')
        self.field_elements['primary_contact']= ui.textarea(label='Primary contact')
        self.field_elements['secondary_contact']= ui.textarea(label='Secondary contact')
        self.field_elements['technical_contact']= ui.textarea(label='Technical contact')
        self.field_elements['client_ID']= ui.textarea(label='Four Digit Client ID')
        self.field_elements['environment_type']= ui.textarea(label='Environment Type')
        self.field_elements['gm_approval']= ui.textarea(label='GM Approval')
        # ... setup and hide all other fields

        # Additional fields for subscriptions
        self.field_elements['aws_account'] = ui.input(label='AWS Account')
        self.field_elements['aws_region'] = ui.input(label='AWS Region')
        self.field_elements['os_type'] = ui.input(label='OS Type')
        self.field_elements['instance_type'] = ui.input(label='Instance Type')

        for element in self.field_elements.values():
            if hasattr(element, 'visible'):
                element.visible = False

        self.update_fields_visibility(self.account_type_switch.value)

        ui.button('Save Details', on_click=self.update_aws_details)

    def on_account_type_change(self, event):
        # This method now receives a switch event, which contains a boolean
        self.update_fields_visibility(event.value)

    def update_fields_visibility(self, is_new_account):
        # Update the visibility of the fields based on the value of the switch
        for field_key in self.new_account_fields:
            if field_key in self.field_elements:
                self.field_elements[field_key].visible = is_new_account
        for field_key in self.subscription_fields:
            if field_key in self.field_elements:
                self.field_elements[field_key].visible = not is_new_account
