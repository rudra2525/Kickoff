from nicegui import app, ui, client

from website.demo import section_window
import myDbConnection
import menu

def network_kickoff(project_det) :

   def delnewVPc():
       print("Deleting VPC")

   def addnewVPc():
       print("Deleting VPC")
   def new_vpc_req():
       print("New VPC Request")
   def new_vpc():
       NewVPCRqstCol = [
           {'headerName': "AWS Account Number", "field": "awsAccNo", 'checkboxSelection': True},
           {'headerName': "Region", "field": "region"},
           {'headerName': "Client Code", "field": "client"},
           {'headerName': "Environment", "field": "Env_Name"},
           {'headerName': "Availablity Zone", "field": "aZone"},
           {'headerName': "Hosted Zone", "field": "hZone"},
       ]
       NewVPCRowDef = []
       NewVPCTable = ui.aggrid({
           'defaultColDef': {'flex': 1},
           'columnDefs': NewVPCRqstCol,
           'rowData': NewVPCRowDef,
           'rowSelection': 'single',
       }).classes('max-h-30')
       vpcDelBtn = ui.button(icon='delete', on_click=delnewVPc)
       with menu.form_card().classes("w-full"):
           with  ui.grid(columns=2).classes("w-full"):
               u_acc_Number  = menu.form_input('AWS Account', "", "pl-6 w-full", "disable")
               u_region      = menu.form_input('AWS Region', "", "pl-6 w-full", "disable")
               u_client      = menu.form_input('Client Code', "", "pl-6 w-full", "disable")
               u_environment = menu.form_input('Environment', "", "pl-6 w-full", "disable")
               u_AZone       = menu.form_input('Availablity Zone', "", "pl-6 w-full")
               u_HZone       = menu.form_input('Hosted Zone', "", "pl-6 w-full")
           vpcAddBtn = ui.button(icon='add', on_click=addnewVPc).classes("w-full")

   def vpc_creation() :
       switch = ui.switch('New VPC?', value=False)
       with ui.column().bind_visibility_from(switch, 'value').classes("w-full"):
            new_vpc()
       with ui.column().bind_visibility_from(switch, 'value', value=False).classes("w-full"):
            ui.label("Test")



    ################ Network Information Tabs ###############################
   with menu.form_card().classes('w-full'):
       with ui.tabs().props('inline-label').classes('bg-primary text-white shadow-2 w-full ') as tabs:
            ui.tab('v', label='VPC Creation', icon='group').classes('w-full')
            ui.tab('p', label='VPC Peering', icon='admin_panel_settings').classes('w-full')
            ui.tab('s', label='Security Group', icon='visibility').classes('w-full')
            ui.tab('4', label='Subnet Creation',icon='visibility').classes('w-full')
            ui.tab('5', label='Private Link',icon='visibility').classes('w-full')
            ui.tab('6', label='Load Balance',icon='visibility').classes('w-full')
            ui.tab('7', label='S3 Access/Endpoint',icon='visibility').classes('w-full')
            ui.tab('8', label='TokenEx ',icon='visibility').classes('w-full')
            ui.tab('9', label='Other Setup',icon='visibility').classes('w-full')
       with ui.tab_panels(tabs, value='v').classes('w-full') as tabpanel:
           with ui.tab_panel('v'):
               vpc_creation()
       with ui.tab_panel('p'):
           vpc_creation()
