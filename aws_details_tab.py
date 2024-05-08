from nicegui import events, ui
import myDbConnection
import menu
import time

def setup_aws_details_tab(client_code=None):
    environment_type_options = myDbConnection.query_allowed_values('ENV_TYPE')
    print(client_code)
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
      switch = ui.switch('New Account', value=False, on_change=lambda value: new_account_ui.set_visibility(value))
      new_account_ui = ui.card().classes('w-full')
      new_account_ui.visible = switch.value
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
                            u_env_type = ui.select(options=environment_type_options, with_input=True, value="", label='Environment Type').classes(f"w-full").props('rounded outlined dense')
                        with aGrptable.cell():
                            u_aws_acc = menu.form_select(aws_account_options, 'AWS Accounts', "", "w-full").props('rounded outlined dense')
                        with aGrptable.cell():
                            u_aws_reg = ui.select(options=aws_region_options, with_input=True, value="", label='AWS Region').classes(f"w-full").props('rounded outlined dense')
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

       def clear_input(input_field):
           input_field.set_value(None)
       with new_account_ui:
           def input_with_delete(label, placeholder):
               with ui.input(placeholder=placeholder).classes('w-full').props('rounded outlined dense') as input_field:
                   delete_button = ui.button(color='469DF9', on_click=lambda: input_field.set_value(None), icon='close').props('flat dense').bind_visibility_from(input_field, 'value')
               return input_field, delete_button

           outlook_distribution_list, outlook_delete_button = input_with_delete("Outlook Distribution List","Enter distribution list email")
           dl_members, dl_members_button = input_with_delete("DL Members", "Enter DL Members")
           account_admin, account_admin_button = input_with_delete("Account Admins", "Enter Account Admins")
           cloud_health_users, cloud_health_users_button = input_with_delete("Cloud Health Users","Enter Cloud Health Users")
           primary_contact, primary_contact_button = input_with_delete("Primary contact", "Enter Primary contact")
           secondary_contact, secondary_contact_button = input_with_delete("Secondary contact","Enter Secondary contact")
           technical_contact, technical_contact_button = input_with_delete("Technical contact","Enter Technical contact")

           def on_validate(value):
               if len(value) != 4:
                   return 'ID must be 4 Digit long'
           client_ID = ui.input(label="Client ID", placeholder="Enter 4 Digit Client ID", validation=on_validate).classes('w-full').props('rounded outlined dense')

           environment_type = ui.select(['Development', 'UAT', 'Production', 'QA'], multiple=True, value=[], label="Environment Type").classes('w-full').props('use-chips''rounded outlined dense')

           gm_approval, gm_approval_button = input_with_delete("GM Approval", "Enter GM Approval")

           save_button = ui.button('Save New Account', on_click=save_details, icon='save')

#setup_aws_details_tab()
#ui.run()
