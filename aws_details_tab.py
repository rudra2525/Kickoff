from nicegui import events, ui
import myDbConnection
import menu
import time

def setup_aws_details_tab(client_code=None):
    #aws_account_container.clear()
    #pClientCode = "STSX"
    environment_type_options = myDbConnection.query_allowed_values('ENV_TYPE')
    if client_code:
        aws_account_options = myDbConnection.query_awsAccount(client_code)
    else:
        aws_account_options = []
    #aws_account_options = myDbConnection.query_awsAccount(pClientCode)
    aws_region_options = myDbConnection.query_awsRegion()
    adGrprows = []

    AdGrpTableCol = [
        {'name': 'Environment_type', 'label': 'Environment Type', 'field': 'Environment_type', 'required': True, 'align': 'left', 'width': '20%', 'headerStyle': 'min-width: 25px'},
        {'name': 'aws_account', 'label': 'AWS Account', 'field': 'aws_account', 'required': True, 'align': 'left', 'width': '20%', 'headerStyle': 'min-width: 25px'},
        {'name': 'aws_region', 'label': 'AWS Region', 'field': 'aws_region', 'required': True, 'align': 'left', 'width': '20%', 'headerStyle': 'min-width: 25px'},
    ]

    def deleteGrp(e: events.GenericEventArguments) -> None:
        nonlocal adGrprows
        adGrprows[:] = [row for row in adGrprows if row["id"] != e.args["id"]]
        ui.notify(f"Delete {e.args['id']}")
        aGrptable.update()

    def print_table_data():
        print("Table Data:")
        for row in adGrprows:
            print(row)


    def save_details():
        data = {
            'Outlook Distribution List': outlook_distribution_list.value,
            'DL Members': dl_members.value,
            'Account Admins': account_admin.value,
            'Cloud Health Users': cloud_health_users.value,
            'Primary contact': primary_contact.value,
            'Secondary contact': secondary_contact.value,
            'Technical contact': technical_contact.value,
            'Digit Client ID': client_ID.value,
            'Environment Type': environment_type.value,
            'GM Approval': gm_approval.value
        }
        print(data)

    def switch_change(value: bool):
        new_account_ui.visible = value

    with ui.card().classes('w-full'):
      switch = ui.switch('New Account', value=False, on_change=switch_change)
      with ui.column().bind_visibility_from(switch, 'value').classes("w-full"):
            with ui.table(columns=AdGrpTableCol, rows=adGrprows).classes('w-full') as aGrptable:
                aGrptable.add_slot(
                    "body",
                    r"""
                    <q-tr :props="props">
                        <q-td key="Environment_type" :props="props" class="w-8 ellipsis">
                            {{ props.row.Environment_type }}
                        </q-td>
                        <q-td key="aws_account" :props="props" class="w-8 ellipsis">
                            {{ props.row.aws_account }}
                        </q-td>
                        <q-td key="aws_region" :props="props" class="w-8 ellipsis">
                            {{ props.row.aws_region }}
                        </q-td>
                        <q-td auto-width>
                            <q-btn size="sm" color="warning" round dense icon="delete" :props="props"
                                @click="() => $parent.$emit('delete', props.row)">
                            </q-btn>
                        </q-td>
                    </q-tr>
                    """,
                )
                with aGrptable.add_slot('bottom-row'):
                    with aGrptable.row():
                        with aGrptable.cell():
                            u_env_type = ui.select(options=environment_type_options, with_input=True, value="", label='Environment Type').classes(f"w-full")
                        with aGrptable.cell():
                            u_aws_acc = menu.form_select(aws_account_options, 'AWS Accounts', "", "w-full")
                        with aGrptable.cell():
                            u_aws_reg = ui.select(options=aws_region_options, with_input=True, value="", label='AWS Region').classes(f"w-full")
                        with aGrptable.cell():
                            ui.button(on_click=lambda: (
                                aGrptable.add_rows({'id': time.time(), 'Environment_type': u_env_type.value, 'aws_account': u_aws_acc.value, "aws_region": u_aws_reg.value}),
                                u_env_type.set_value(None),
                                u_aws_acc.set_value(None),
                                u_aws_reg.set_value(None)
                            ), icon='add')

                    aGrptable.on("delete", deleteGrp)
            ui.button('Save', on_click=print_table_data, icon='save')

      with ui.column().bind_visibility_from(switch, 'value', value=False).classes("w-full"):
       new_account_ui = ui.card().bind_visibility_from(switch, 'value', value=False).classes('w-full')

       with new_account_ui:
           outlook_distribution_list = ui.input(label="Outlook Distribution List",
                                                placeholder="Enter distribution list email").classes('w-full')
           dl_members = ui.input(label="DL Members", placeholder="Enter DL Members").classes('w-full')
           account_admin = ui.input(label="Account Admins", placeholder="Enter Account Admins").classes('w-full')
           cloud_health_users = ui.input(label="Cloud Health Users", placeholder="Enter Cloud Health Users").classes(
               'w-full')
           primary_contact = ui.input(label="Primary contact", placeholder="Enter Primary contact").classes('w-full')
           secondary_contact = ui.input(label="Secondary contact", placeholder="Enter Secondary contact").classes(
               'w-full')
           technical_contact = ui.input(label="Technical contact", placeholder="Enter Technical contact").classes(
               'w-full')
           client_ID = ui.input(label="Digit Client ID", placeholder="Enter Digit Client ID").classes('w-full')
           environment_type = ui.input(label="Environment Type", placeholder="Enter Environment Type").classes('w-full')
           gm_approval = ui.input(label="GM Approval", placeholder="Enter GM Approval").classes('w-full')
           ui.button('Save New Account', on_click=save_details, icon='save')

#setup_aws_details_tab()
#ui.run()
