from nicegui import events, ui, app
import myDbConnection
import menu
import time
from website.demo import bash_window
import asyncio
import json


def setup_aws_details_tab(client_code=None):
    environment_type_options = myDbConnection.query_allowed_values('ENV_TYPE') or []
    client_code = client_code or 'STSX'
    aws_account_options = myDbConnection.query_awsAccount(client_code) or []
    aws_region_options = myDbConnection.query_awsRegion() or []

    aws_details_row = app.storage.aws_details

    

    def oldAWS():
        def save_aws_details():
            new_detail = {
                'id': time.time(),
                'environment_type': env_type_select.value,
                'aws_acc': aws_acc_select.value,
                'aws_region': aws_region_select.value
            }
            aws_details_row.append(new_detail)
            app.storage.aws_details = aws_details_row
            awsDetailsTable.options['rowData'] = aws_details_row
            awsDetailsTable.update()
            awsDetailsDialog.close()

        async def edit_aws_details():
            selected_row = await awsDetailsTable.get_selected_row()
            if selected_row:
                for i, row in enumerate(aws_details_row):
                    if row['id'] == selected_row['id']:
                        aws_details_row[i] = {
                            'id': row['id'],
                            'environment_type': env_type_select.value,
                            'aws_acc': aws_acc_select.value,
                            'aws_region': aws_region_select.value
                        }
                        break
                app.storage.aws_details = aws_details_row
                awsDetailsTable.options['rowData'] = aws_details_row
                awsDetailsTable.update()
                awsDetailsDialog.close()
            else:
                ui.notify("No row selected for editing", type='warning')

        async def remove_aws_details():
            selected_row = await awsDetailsTable.get_selected_row()
            if selected_row:
                aws_details_row[:] = [row for row in aws_details_row if row['id'] != selected_row['id']]
                app.storage.aws_details = aws_details_row
                awsDetailsTable.options['rowData'] = aws_details_row
                awsDetailsTable.update()
                ui.notify("Row removed successfully", type='positive')
            else:
                ui.notify("No row selected for removal", type='warning')

        def save_all_details():
            print("AWS Details:")
            for row in aws_details_row:
                print(row)
            ui.notify("Data Saved", type='positive')

        with ui.dialog() as awsDetailsDialog:
            with bash_window("Add Server Detail", classes='w-full'):
                with ui.grid(columns=2).classes('gap-4'):
                    env_type_select = ui.select(options=environment_type_options, label='Environment Type').classes('pl-6 w-5/6')
                    aws_acc_select = ui.select(options=aws_account_options, with_input=True, value="", label='Aws Account').classes('pl-6 w-5/6')
                    aws_region_select = ui.select(options=aws_region_options, label='AWS Region').classes('pl-6 w-5/6')

                with ui.row().classes('self-center place-items-center'):
                    ui.button('Add', on_click=save_aws_details, icon='add').classes('m-2')
                    ui.button('Close', on_click=awsDetailsDialog.close, icon='close').classes('m-2')

        aws_details_columns = [
            {'headerName': '', 'checkboxSelection': True, 'width': 50},  # Add checkbox selection
            {'headerName': 'Environment Type', 'field': 'environment_type'},
            {'headerName': 'Aws Account', 'field': 'aws_acc'},
            {'headerName': 'Aws Region', 'field': 'aws_region'}
        ]

        with ui.card().classes('w-full'):
            with ui.row().classes('w-full'):
                awsDetailsTable = ui.aggrid({
                    'defaultColDef': {'flex': 1},
                    'columnDefs': aws_details_columns,
                    'rowData': aws_details_row,
                    'rowSelection': 'single'
                }).classes('w-full')

            with ui.row().classes('self-center place-items-center'):
                ui.button('Add', on_click=awsDetailsDialog.open, icon='add').classes('m-2')
                ui.button('Edit', on_click=lambda: asyncio.create_task(edit_aws_details()), icon='edit').classes('m-2')
                ui.button('Delete', on_click=lambda: asyncio.create_task(remove_aws_details()), icon='delete').classes('m-2')
                ui.button('Save', on_click=save_all_details, icon='save').classes('m-2')

    def save_details():
        data = {
            "Outlook Distribution List": outlook_distribution_list.value,
            'DL Members': dl_members.value,
            'Account Admins': account_admin.value,
            'Cloud Health Users': cloud_health_users.value,
            'Primary contact': primary_contact.value,
            'Secondary contact': secondary_contact.value,
            'Technical contact': technical_contact.value,
            'Digit Client ID': client_ID.value,
            'Environment Type': environment_type.value,
            'AWS Region': region.value,
            'GM Approval': gm_approval.value
        }

        file_name = 'NewAWS.json'
        with open(file_name, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        with open(file_name, 'r') as json_file:
            aws_acc_attr_content = json_file.read()

        print(f"Data has been saved to {file_name}")

    switch = ui.switch("New AWS Account", value=False)

    with ui.column().bind_visibility_from(switch, 'value').classes('w-full'):
        def input_with_delete(label, placeholder):
            with ui.input(placeholder=placeholder).classes('w-full').props('rounded outlined dense') as input_field:
                delete_button = ui.button(color='469DF9', on_click=lambda: input_field.set_value(None), icon='close').props('flat dense').bind_visibility_from(input_field, 'value')
            return input_field, delete_button

        outlook_distribution_list, outlook_delete_button = input_with_delete("Outlook Distribution List", "Enter distribution list email")
        dl_members, dl_members_button = input_with_delete("DL Members", "Enter DL Members")
        account_admin, account_admin_button = input_with_delete("Account Admins", "Enter Account Admins")
        cloud_health_users, cloud_health_users_button = input_with_delete("Cloud Health Users", "Enter Cloud Health Users")
        primary_contact, primary_contact_button = input_with_delete("Primary contact", "Enter Primary contact")
        secondary_contact, secondary_contact_button = input_with_delete("Secondary contact", "Enter Secondary contact")
        technical_contact, technical_contact_button = input_with_delete("Technical contact", "Enter Technical contact")

        def on_validate(value):
            if len(value) != 4:
                return 'ID must be 4 Digit long'

        client_ID = ui.input(label="Client ID", placeholder="Enter 4 Digit Client ID", validation=on_validate).classes('w-full').props('rounded outlined dense')
        environment_type = ui.select(['Development', 'UAT', 'Production', 'QA'], multiple=True, value=[], label="Environment Type").classes('w-full').props('use-chips rounded outlined dense')
        region = ui.select(options=aws_region_options, label='AWS Region').classes('w-full').props('use-chips rounded outlined dense')
        gm_approval, gm_approval_button = input_with_delete("GM Approval", "Enter GM Approval")

        save_button = ui.button('Save New Account', on_click=save_details, icon='save')

    with ui.column().bind_visibility_from(switch, 'value', value=False).classes('w-full'):
        oldAWS()
