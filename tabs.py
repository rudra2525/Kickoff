from nicegui import ui
#from aws_details_tab import setup_aws_details_tab
from aws_details_tab import AwsDetailsForm
from search_and_details import setup_project_dropdown, jira
from NetworkTab import NetworkDetailsForm
from ProjectDet import ProjecDetail
import requests
from website.demo import section_window

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
# Sample ProjDetail data
ProjDetail = {
    "summary": "Project Name",
    "jirakey": "Jira Key",
    "Projecttype": "Project Type",
    "platform": "Platform",
    "Location": "Location",
    "ClientCode": "Client Code",
    "Bustechowner": "Tech Owner",
    "Techlead": "Tech Lead",
    "DBAlead": "DBA Lead",
    "eEnvironment": "Environment Type",
    "Objective": "Objective",
    # Add other fields here...
}
aws_details_form = AwsDetailsForm()
network_details_form = NetworkDetailsForm()
ui.label('Project Intake Form').classes('text-h3 py-4').style('text-align: center; width: 100%;')
setup_project_dropdown(jira, ui, aws_details_form)
ProjecDetail(ProjDetail)



form_data = {}
with ui.splitter(value=10).classes('w-full h-full') as splitter:
    with splitter.before:
        with ui.tabs().props('vertical').classes('w-full') as tabs:
            #general_info = ui.tab('General Information', icon='info')
            aws_details = ui.tab('AWS Details', icon='cloud')
            network_info = ui.tab('Network Information', icon='router')
            server_details = ui.tab('Server Details', icon='dns')
            user_info = ui.tab('User Information', icon='person')
            patching_info = ui.tab('Patching Information', icon='healing')
            monitoring_info = ui.tab('Monitoring Information', icon='visibility')
            backup_info = ui.tab('Back Information', icon='backup')
            custom_spec = ui.tab('Custom Spec', icon='list')
            firewall_req = ui.tab('Firewall Requirement', icon='shield')
            # Add more tabs as needed...

    with splitter.after:
        with ui.tab_panels(tabs, value=aws_details).props('vertical').classes('w-full h-full'):

            with ui.tab_panel(aws_details):
                #ui.label('AWS Account').classes('text-h4')
                with section_window("AWS Account", classes='w-full'):
                    aws_details_form.setup_aws_details_tab()
                    ui.button('Save Details', on_click=aws_details_form.update_form_data)

            with ui.tab_panel(network_info):
                ui.label('Network Information').classes('text-h4')
                network_details_form.setup_NetworkTab()
                ui.button('Save Details', on_click=network_details_form.update_network_details)
            # Define more tab panels for other tabs...

ui.run(title='Project Kickoff UI', port=8082)
