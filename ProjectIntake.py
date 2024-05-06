import theme
from nicegui import Client, APIRouter, ui
import menu
from jira import JIRA
from aws_details_tab import setup_aws_details_tab
from website.demo import section_window
from NetworkTab import NetworkDetailsForm

network_details_form = NetworkDetailsForm()


class ProjectIntake():

    def __init__(self) -> None:

        super().__init__()

        vProject = ""

        def GetProjectList():
            userName = menu.getJsonVal("env_var", "JIRAUSER")
            passWord = menu.getJsonVal("env_var", "JIRAPASS")
            urlPath = menu.getJsonVal("env_var", "JIRAURL")
            jqlStr = menu.getJsonVal("env_var", "KICKOFF")

            jiraOptions = {'server': urlPath, 'verify': False}
            jira = JIRA(options=jiraOptions, basic_auth=(userName, passWord))
            issueList = jira.search_issues(jqlStr)
            nProjList = []  # New project  from Jira
            for singleIssue in issueList:
                issue_info = singleIssue.key + "—" + singleIssue.fields.summary
                nProjList.append(issue_info)

            return nProjList

        def getJiraProjInfo(projKey):
            userName = menu.getJsonVal("env_var", "JIRAUSER")
            passWord = menu.getJsonVal("env_var", "JIRAPASS")
            urlPath = menu.getJsonVal("env_var", "JIRAURL")
            jqlStr = f"key = '{projKey}'"
            jiraOptions = {'server': urlPath, 'verify': False}
            jira = JIRA(options=jiraOptions, basic_auth=(userName, passWord))
            issueList = jira.search_issues(jqlStr)

            for singleIssue in issueList:
                components = singleIssue.fields.components
                Location = singleIssue.fields.customfield_41320
                if singleIssue.fields.customfield_17322:
                    ProjectType = singleIssue.fields.customfield_17322.value
                else:
                    ProjectType = None
                ClientCode = singleIssue.fields.customfield_45567
                TechOwner = singleIssue.fields.customfield_55222
                TechLead = singleIssue.fields.customfield_59620
                DBALead = singleIssue.fields.customfield_59621
                eEnvironment = singleIssue.fields.customfield_59622
                BusinessArea = singleIssue.fields.customfield_53524
                GOLiveEmail = singleIssue.fields.customfield_59623
                print(ClientCode)

                issue_info = {'jirakey': singleIssue.key,
                              'summary': singleIssue.fields.summary,
                              'ClientCode': ClientCode if ClientCode else 'None',
                              'Projecttype': ProjectType if ProjectType else 'None',
                              'platform': components[0].name if components else 'None',
                              'Location': Location[0].value if Location else 'None',
                              'eEnvironment': eEnvironment if eEnvironment else 'None',
                              'BussinessArea': BusinessArea if BusinessArea else 'None',
                              'Bustechowner': TechOwner if TechOwner else 'None',
                              'Techlead': TechLead if TechLead else 'None',
                              'DBAlead': DBALead if DBALead else 'None',
                              'goLiveEmail': GOLiveEmail if GOLiveEmail else 'None',
                              }

            return issue_info

        def set_projDet(event):
            if event.value:
                jiraval = event.value.split("—", 1)
                if len(jiraval) > 1:
                    jiraKey = jiraval[0]
                    ProjInfo = getJiraProjInfo(jiraKey)
                    u_jira_key.set_value(jiraKey)
                    u_proj_type.set_value(ProjInfo['Projecttype'])
                    u_platform.set_value(ProjInfo['platform'])
                    u_location.set_value(ProjInfo['Location'])
                    u_client.set_value(ProjInfo['ClientCode'])
                    u_techowner.set_value(ProjInfo['Bustechowner'])
                    u_techlead.set_value(ProjInfo['Techlead'])
                    u_DBAlead.set_value(ProjInfo['DBAlead'])
                    u_eEnvType.set_value(ProjInfo['eEnvironment'])
                    u_BusArea.set_value(ProjInfo['BussinessArea'])
                    u_GOLiveEmail.set_value(ProjInfo['goLiveEmail'])
                    clientCode = ProjInfo['ClientCode']
                    u_client.set_value(clientCode)

                    clientCode = ProjInfo['ClientCode']
                    u_client.set_value(clientCode)
                    if clientCode:
                        setup_aws_details_tab(client_code=clientCode)

        with theme.frame('Project Intake /Kick Off'):
            with section_window("Project Details", classes='w-full h-60'):
                with  ui.grid(columns=4):
                    projectList = GetProjectList()
                    u_project = ui.select(options=projectList, with_input=True, value="", label='Select a Project',
                                          on_change=set_projDet).classes(" q-pa-none pl-6 w-64 mr-2")
                    u_jira_key = menu.form_input('Jira Key', "", " q-pa-none pl-6 w-64 mr-2", "disable")
                    u_proj_type = menu.form_input('Project Type', "", " q-pa-none pl-6 w-64 mr-2", "disable")
                    u_platform = menu.form_input('Platform', "", " q-pa-none pl-6 w-64 mr-2", "disable")
                    u_location = menu.form_input('Location', "", " q-pa-none pl-6 w-64 mr-2", "disable")
                    u_client = menu.form_input('Client Code', "", " q-pa-none pl-6 w-64 mr-2", "disable")
                    u_techowner = menu.form_input('Tech Owner', "", " q-pa-none pl-6 w-64 mr-2", "disable")
                    u_techlead = menu.form_input('Tech Lead', "", " q-pa-none pl-6 w-64 mr-2", "disable")
                    u_DBAlead = menu.form_input('DBA Lead', "", " q-pa-none pl-6 w-64 mr-2", "disable")
                    u_eEnvType = menu.form_input('Environment Type', "", " q-pa-none pl-6 w-64 mr-2", "disable")
                    u_BusArea = menu.form_input('Business Area', "", " q-pa-none pl-6 w-64 mr-2", "disable")
                    with ui.expansion('Go Live Communication Email List!', icon='email').classes('w-full'):
                        u_GOLiveEmail = menu.form_textarea('', "", " q-pa-none pl-6 w-80 h-1")
            with ui.splitter(value=10).classes('w-full h-full') as splitter:
                with splitter.before:
                    with ui.tabs().props('vertical').classes('w-full') as tabs:
                        # general_info = ui.tab('General Information', icon='info')
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
                            # ui.label('AWS Account').classes('text-h4')
                            with section_window("AWS Account", classes='w-full'):
                                setup_aws_details_tab()

                            # aws_details_form.setup_aws_details_tab()
                            # ui.button('Save Details', on_click=aws_details_form.update_form_data)

                        with ui.tab_panel(network_info):
                            with section_window("Network Information", classes='w-full'):
                                with ui.grid(columns=4, rows=4).classes('w-full'):
                                    network_details_form.setup_VPC_Creation()
                                    network_details_form.setup_VPC_Peering()
                                    network_details_form.setup_Security_Group_Creation()
                                    network_details_form.setup_AWS_Firewall_Request()
                                    network_details_form.setup_Port_Open_Request()
                                    network_details_form.setup_Subnet_Creation()
                                    network_details_form.setup_Private_Link()
                                    network_details_form.setup_Load_Balancer()
                                    network_details_form.setup_ELB()
                                    network_details_form.setup_ALB()
                                    network_details_form.setup_NLB()
                                    network_details_form.setup_S3_Access()
                                    network_details_form.setup_TokenEx()
                                    network_details_form.setup_Other()
                            network_details_form.button()
                        # ui.button('Save Details', on_click=network_details_form.update_network_details).style('position: fixed; left: 100px; bottom: 50px;')
                        # Define more tab panels for other tabs
