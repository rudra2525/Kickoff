from nicegui import ui


class NetworkDetailsForm:

    def __init__(self):
        self.form_data = {}
        self.AWS_acct_number = None
        self.Region = None
        self.Client_Code = None
        self.Client_Env = None
        self.Avail_zones = None
        self.Hosted_Zones = None
        self.VPC_Name = None
        self.VPC_ID = None
        self.IPv4_CIDR_Blk = None
        self.AWS_Public_CIDR = None
        self.AWS_Private_CIDR = None

    @staticmethod
    def get_stored_data():
        return {
            'Outlook Distribution list': 'Azure-VANG-DEV@epsilon.com',
            'DL Members': 'user1@example.com, user2@example.com',
            'Account Admins': 'admin@gmail.com',
            'Cloud Health Users': 'health@gmail.com',
            'Accounting Cost Center': 'US1802:4210100000:1A6F010198:B1A6F-002683-00:::P01017',

            #'GM Approval': 'gm@gmail.com',
            # ... [other fields]
        }

    def update_form_data(self, event=None):
        # Implementation to update form_data based on the input fields
        self.form_data['AWS Account Number:'] = self.AWS_acct_number.value
        self.form_data['Region:'] = self.Region.value
        self.form_data['Client Code:'] = self.Client_Code.value
        self.form_data['Client Env:'] = self.Client_Env.value
        self.form_data['Availability Zones'] = self.Avail_zones.value
        self.form_data['Hosted Zone'] = self.Hosted_Zones.value
        self.form_data['VPC Name:'] = self.VPC_Name.value
        self.form_data['VPC ID:'] = self.VPC_ID.value
        self.form_data['IPv4 CIDR Block:'] = self.IPv4_CIDR_Blk.value
        self.form_data['AWS Public CIDR:'] = self.AWS_Public_CIDR.value
        self.form_data['AWS Private CIDR:'] = self.AWS_Private_CIDR.value

    def update_network_details(self, event):
        # Update form_data with the values from inputs
        self.form_data['network_details'] = {  # Collect all AWS details
            'account_type': self.NewAccount.value
            # ... [other fields as needed]
        }




    def setup_NetworkTab(self):
        with ui.row():
            with ui.card().classes("w-full"):
                NewAccount = ui.switch('New VPC?', value=True).classes('w-60')
                with ui.column().bind_visibility_from(NewAccount, 'value').classes("w-full"):
                    self.AWS_acct_number = ui.input(label='AWS Account Number:').classes('w-full')
                    self.Region = ui.input(label='Region:').classes('w-full')
                    self.Client_Code = ui.input(label='Client Code:').classes('w-full')
                    self.Client_Env = ui.input(label='Client Env:').classes('w-full')
                    self.Avail_zones = ui.input(label='Availability Zones:').classes('w-full')
                    self.Hosted_Zones = ui.input(label='Hosted Zones:').classes('w-full')

                    ui.button('Save Changes')
                with ui.column().bind_visibility_from(NewAccount, 'value', value=False).classes("w-full"):
                    self.get_stored_data()
                    self.VPC_Name = ui.input(label='VPC Name:').classes('w-full')
                    self.VPC_ID = ui.input(label="VPC ID:").classes('w-full')
                    self.IPv4_CIDR_Blk = ui.input(label='IPv4 CIDR Block:').classes('w-full')
                    self.AWS_Public_CIDR = ui.input(label='AWS Public CIDR').classes('w-full')
                    self.AWS_Private_CIDR = ui.input(label='AWS Private CIDR').classes('w-full')

                    ui.button('Save Changes')
