from nicegui import ui, app
import ProjectIntake
import theme
import ProjectDet
import TreeMenu
import Ec2Provisioning
import myDbConnection
import bldServerlist
import menu
from AWSAccounts import AWSAccount
from ProjectInfo import ProjectInfo
from nicegui import Client, APIRouter
from website.demo import section_window
from aws_details_tab import setup_aws_details_tab
import NetworkTab
from patching_dal import setup_patching
from monitoring import setup_monitoring
from service_account import setup_service_acc
from backup_info import setup_backup_info
from custom_spec import setup_custSpec_info
from serverDetail import setup_serverDetail

def initialize_storage():
    try:
        _ = app.storage.aws_details
    except AttributeError:
        app.storage.aws_details = []

    try:
        _ = app.storage.network_info
    except AttributeError:
        app.storage.network_info = []

    try:
        _ = app.storage.server_details
    except AttributeError:
        app.storage.server_details = []

    try:
        _ = app.storage.user_info
    except AttributeError:
        app.storage.user_info = []

    try:
        _ = app.storage.patching_info
    except AttributeError:
        app.storage.patching_info = []

    try:
        _ = app.storage.monitoring_info
    except AttributeError:
        app.storage.monitoring_info = []

    try:
        _ = app.storage.service_acc_info
    except AttributeError:
        app.storage.service_acc_info = []

    try:
        _ = app.storage.backup_info
    except AttributeError:
        app.storage.backup_info = []

    try:
        _ = app.storage.custom_spec
    except AttributeError:
        app.storage.custom_spec = []

    try:
        _ = app.storage.firewall_req
    except AttributeError:
        app.storage.firewall_req = []

initialize_storage()
project_key = ""

@ui.page('/ProjectIntake')
def ProjIntake(client: Client):
    projectList = menu.GetProjectList("KICKOFF")


    def set_projDet(event):
        if event.value:
            jiraval = event.value.split("—", 1)
            if len(jiraval) > 1:
                with client.content:
                    ui.html(f'<h1>You chose {jiraval}</h1>')
                    jiraKey = jiraval[0]
                    ProjInfo = menu.getJiraProjInfo(jiraKey)
                    client.content.clear()
                    print(ProjInfo)  # Debugging: print the ProjInfo dictionary to inspect its structure
                    clientCode = ProjInfo.get('ClientCode', '')
                    envName = ProjInfo.get('EnvName', '')  # Use .get() to safely access keys

                    ProjectIntake.ProjectIntake(ProjInfo, tabs, aws_details, network_info)
                    with ui.tab_panels(tabs, value=aws_details).props('vertical').classes('w-full h-full'):
                        environment_type_options = myDbConnection.query_allowed_values('ENV_TYPE') or []
                        with ui.tab_panel(aws_details):
                            with section_window("AWS Account", classes='w-full'):
                                if clientCode:
                                    setup_aws_details_tab(clientCode, ProjDetail=ProjInfo, awsDetail=aws_details)
                        with ui.tab_panel(network_info):
                            with section_window("Network Information", classes='w-full'):
                                NetworkTab.network_kickoff(ProjInfo)
                        with ui.tab_panel(server_details):
                            with section_window("Server Details", classes='w-full'):
                                setup_serverDetail(ProjDetail=ProjInfo)
                        with ui.tab_panel(user_info):
                            with section_window("AD User Access", classes='w-full'):
                                ui.label("AD User Access")  # Replace this with AD User Access Module
                        with ui.tab_panel(patching_info):
                            with section_window("Patching Requirements", classes='w-full'):
                                setup_patching(ProjDetail=ProjInfo)
                        with ui.tab_panel(monitoring_info):
                            with section_window("Monitoring Requirements", classes='w-full'):
                                setup_monitoring(ProjDetail=ProjInfo)
                        with ui.tab_panel(serviceAcc_info):
                            with section_window("Service Accounts Requirements", classes='w-full'):
                                setup_service_acc(ProjDetail=ProjInfo)
                        with ui.tab_panel(backup_info):
                            with section_window("Backup Requirements", classes='w-full'):
                                setup_backup_info(ProjDetail=ProjInfo)
                        with ui.tab_panel(custom_spec):
                            with section_window("Custom Specs Requirements", classes='w-full'):
                                setup_custSpec_info(ProjDetail=ProjInfo)
                        with ui.tab_panel(firewall_req):
                            with section_window("Firewall Requirements", classes='w-full'):
                                ui.label("Firewall Requirements")  # Replace this with Firewall module

    with theme.frame('Project Kickoff'):
        with ui.left_drawer().style('background-color: #F8F8F8').props("elevated v-model='leftDrawerOpen'"):
            u_project = ui.select(options=projectList, with_input=True, value="", label='Select a Project', on_change=set_projDet).classes(" q-pa-none pl-6 w-64 mr-2")
            ui.separator()
            with ui.tabs().props('vertical').classes('w-full') as tabs:
                aws_details = ui.tab('AWS Details', icon='cloud')
                network_info = ui.tab('Network Information', icon='router')
                server_details = ui.tab('Server Details', icon='dns')
                user_info = ui.tab('User Information', icon='person')
                patching_info = ui.tab('Patching Information', icon='healing')
                monitoring_info = ui.tab('Monitoring Information', icon='visibility')
                serviceAcc_info = ui.tab('Service Accounts Information', icon='smart_toy')
                backup_info = ui.tab('Backup Information', icon='backup')
                custom_spec = ui.tab('Custom Spec', icon='list')
                firewall_req = ui.tab('Firewall Requirement', icon='shield')


@ui.page('/EC2provisioning')
def ec2Provisioning(client: Client):
    def savedata(ProjectId, buildServer):
        if buildServer:
            ui.open(f"/bldservers?ProjectId={ProjectId}")
        else:
            ec2page.refresh()

    def treeSelect(treeNode):
        with client.content:
            ui.html(f'<h1>You chose {treeNode}</h1>')
            if len(treeNode) == 2:
                ProjInfo = ProjectInfo()
                ProjDetail = ProjInfo.getProjectInfo(treeNode)
                client.content.clear()
                ProjectDet.ProjecDetail(ProjDetail)
                Ec2Provisioning.awsServers(ProjDetail, savedata)

    @ui.refreshable
    def ec2page():
        treeNode = []
        with theme.frame('EC2 Provisioning'):
            with ui.left_drawer().style('background-color: #F8F8F8').props("elevated v-model='leftDrawerOpen'"):
                TreeMenu.buildTreeMenu(treeSelect, treeNode)

    ec2page()

@ui.page('/bldservers')
def bldServers(ProjectId: str = None):
    ec2RowDef = myDbConnection.query_server_det(ProjectId)

    ec2ColDef = [
        {'headerName': "Host Name ", "field": "Host_Name", 'headerCheckboxSelection': True, 'checkboxSelection': True},
        {'headerName': "Client Code", "field": "ClientCode"},
        {'headerName': "Acc. Name", "field": "AccName"},
        {'headerName': "Acc. Number", "field": "AccNumber"},
        {'headerName': "Region", "field": "Region"},
        {'headerName': "OS Type", "field": "osType"},
        {'headerName': "Instance Type", "field": "instantType"},
        {'headerName': "VPC Info", "field": "VPCInfo"},
        {'headerName': "Subnet", "field": "Subnet"},
    ]

    async def bldSelSrv():
        if u_email_id.value:
            Srvlist = await ec2Table.get_selected_rows()
            if Srvlist:
                bldServerlist.bldSrvList(Srvlist, u_email_id.value)
            else:
                ui.notify("No Server Select for Build", type='negative')
        else:
            ui.notify("No Email Address to send Communication", type='negative')

    with theme.frame('Server Build'):
        with section_window("EC2 Server Details", classes='w-full'):
            with ui.row().classes("w-full"):
                u_email_id = menu.form_input('Enter Email Id for Build Results', "", "pl-6 w-full")
            with ui.row().classes("w-full"):
                ui.label("Select the Server below for Provisioning").classes('pl-6 w-5/6 font-bold mb-3')
                with ui.row().classes("w-full"):
                    ec2Table = ui.aggrid({
                        'defaultColDef': {'flex': 1},
                        'columnDefs': ec2ColDef,
                        'rowData': ec2RowDef,
                        'rowSelection': 'multiple',
                        'masterDetail': True,
                    }).classes('pl-6 pr-6 max-h-full')
        with ui.row().classes("w-full pl-6"):
            ui.button('Provision Servers', icon='construction', on_click=bldSelSrv)
            ui.button('Close', icon='close', on_click=lambda: ui.open("/"))
