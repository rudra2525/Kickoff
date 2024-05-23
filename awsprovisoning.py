from nicegui import ui
import ProjectIntake
import theme
import ProjectDet
import TreeMenu
import Ec2Provisioning
#import ViewBuildInfo
import myDbConnection
import bldServerlist
import menu
from AWSAccounts import AWSAccount

from ProjectInfo import ProjectInfo
from nicegui import Client, APIRouter, ui
from website.demo import section_window
from aws_details_tab import setup_aws_details_tab
from Server_detail import setup_server_details
import NetworkTab


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
                  clientCode  = ProjInfo['ClientCode']
                  ProjectIntake.ProjectIntake(ProjInfo,tabs,aws_details,network_info)
                  with ui.tab_panels(tabs, value=aws_details).props('vertical').classes('w-full h-full'):
                      with ui.tab_panel(aws_details):
                          with section_window("AWS Account", classes='w-full'):
                              if clientCode:
                                 setup_aws_details_tab(clientCode)
                      with ui.tab_panel(network_info):
                          with section_window("Network Information", classes='w-full'):
                              NetworkTab.network_kickoff(ProjInfo)
                      with ui.tab_panel(server_details):
                          with section_window("Server Details ", classes='w-full'):
                                  setup_server_details(on_saverow=callable)
                      with ui.tab_panel(user_info):
                          with section_window("AD User Access", classes='w-full'):
                                  ui.label("AD User Access") # Replace this with AD USer Access Module
                      with ui.tab_panel(patching_info):
                          with section_window("Patching Requirements", classes='w-full'):
                                  ui.label("Patching Requirements") # Replace this with Patching Module
                      with ui.tab_panel(monitoring_info):
                          with section_window("Monitoring Requirements", classes='w-full'):
                                  ui.label("Monitoring Requirements") # Replace this with Monitoring Module
                      with ui.tab_panel(serviceAcc_info):
                          with section_window("Service Accounts Requirements", classes='w-full'):
                              ui.label("Service Accounts Requirements") # Replace this with Service Accounts Module
                      with ui.tab_panel(backup_info):
                          with section_window("Backup Requirments", classes='w-full'):
                              ui.label("Backup Requirments")  # Replace this with Backup module
                      with ui.tab_panel(custom_spec):
                          with section_window("Custom Specs Requirments", classes='w-full'):
                              ui.label("Custom Spect Requirments")  # Replace this with Custom specs  module
                      with ui.tab_panel(firewall_req):
                          with section_window("Firewall Requirements", classes='w-full'):
                              ui.label("Firewall Requirements")  # Replace this with FireWall  module

  with theme.frame('Project Kickoff '):
      with ui.left_drawer().style('background-color: #F8F8F8').props("elevated v-model='leftDrawerOpen'"):
           u_project = ui.select(options=projectList, with_input=True, value="", label='Select a Project', on_change=set_projDet).classes(" q-pa-none pl-6 w-64 mr-2")
           ui.separator()
           with ui.tabs().props('vertical').classes('w-full') as tabs:
               # general_info = ui.tab('General Information', icon='info')
               aws_details = ui.tab('AWS Details', icon='cloud')
               network_info = ui.tab('Network Information', icon='router')
               server_details = ui.tab('Server Details', icon='dns')
               user_info = ui.tab('User Information', icon='person')
               patching_info = ui.tab('Patching Information', icon='healing')
               monitoring_info = ui.tab('Monitoring Information', icon='visibility')
               serviceAcc_info = ui.tab('Service Accounts Information', icon='smart_toy')
               backup_info = ui.tab('Back Information', icon='backup')
               custom_spec = ui.tab('Custom Spec', icon='list')
               firewall_req = ui.tab('Firewall Requirement', icon='shield')
           # Add more tabs as needed...



@ui.page('/EC2provisoning')
#@router.page('/')


def ec2Provisioning(client: Client) :
    def savedata(ProjectId,buildServer ):
       if buildServer :
          ui.open(f"/bldservers?ProjectId={ProjectId}")
       else :
          ec2page.refresh()

    def treeSelect(treeNode):
        with client.content:
            ui.html(f'<h1>You chose {treeNode}</h1>')
            if len(treeNode) == 2 :
                 ProjInfo = ProjectInfo()
                 ProjDetail = ProjInfo.getProjectInfo(treeNode)
                 client.content.clear()
                 ProjectDet.ProjecDetail(ProjDetail)
                 Ec2Provisioning.awsServers(ProjDetail,savedata)

    @ui.refreshable
    def ec2page() :
       treeNode = []
       with theme.frame('EC2 Provisioning'):
         with ui.left_drawer().style('background-color: #F8F8F8').props("elevated v-model='leftDrawerOpen'"):
             TreeMenu.buildTreeMenu(treeSelect,treeNode)

    ec2page()

@ui.page('/bldservers')
#@router.page('/bldservers')

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

  async def bldSelSrv() :
        if u_email_id.value:
            Srvlist  = await ec2Table.get_selected_rows()
            if  Srvlist:
                bldServerlist.bldSrvList(Srvlist, u_email_id.value)
            else:
                ui.notify("No Server Select for Build ", type='negative')
        else :
             ui.notify("No Email Address to send Communication ", type='negative')


  with theme.frame('Server Build'):
    with section_window("EC2 Server Details", classes='w-full'):
      with ui.row().classes("w-full"):
           u_email_id  = menu.form_input('Enter Email Id for Build Results', "","pl-6 w-full")
      with ui.row().classes("w-full"):
          ui.label("Select the Server below for Provisioning").classes('pl-6 w-5/6 font-bold mb-3')
          with ui.row().classes("w-full"):
              ec2Table = ui.aggrid({
                  'defaultColDef': {'flex': 1},
                  'columnDefs': ec2ColDef,
                  'rowData': ec2RowDef,
                  'rowSelection': 'multiple',
                  'masterDetail': True,
              }).classes('pl-6  pr-6 max-h-full')
    with ui.row().classes("w-full pl-6"):
         ui.button('Provision Servers', icon='construction', on_click= bldSelSrv)
         ui.button('Close', icon='close', on_click= lambda: ui.open("/"))
