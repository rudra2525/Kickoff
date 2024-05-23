import asyncio
from nicegui import events, ui
import myDbConnection
import menu
import time
from website.demo import bash_window


def setup_server_details(on_saverow: callable):
    # Fetch data from database
    Os_type_option = myDbConnection.query_os_type()
    Instance_type_option = myDbConnection.query_allowed_values('AWS_INSTANCE')

    server_details_rows = []

    def save_server_details():
        server_details = {
            'id': time.time(),  # Unique ID for each row
            'Os_type': os_type_select.value,
            'instance_type': instance_type_select.value,
            'server_prefix': server_prefix_input.value,
            'Server_sequence_number': server_seq_num_input.value,
            'Quantity': quantity_input.value,
            'Subnet_information': subnet_info_input.value
        }
        server_details_rows.append(server_details)
        serverDetailsTable.options['rowData'] = server_details_rows
        serverDetailsTable.update()
        serverDetailsDialog.close()

    async def edit_server_details():
        selected_row = await serverDetailsTable.get_selected_row()
        if selected_row:
            for i, row in enumerate(server_details_rows):
                if row['id'] == selected_row['id']:
                    server_details_rows[i] = {
                        'id': row['id'],
                        'Os_type': os_type_select.value,
                        'instance_type': instance_type_select.value,
                        'server_prefix': server_prefix_input.value,
                        'Server_sequence_number': server_seq_num_input.value,
                        'Quantity': quantity_input.value,
                        'Subnet_information': subnet_info_input.value
                    }
                    break
            serverDetailsTable.options['rowData'] = server_details_rows
            serverDetailsTable.update()
            serverDetailsDialog.close()
        else:
            ui.notify("No row selected for editing", type='warning')

    async def remove_server_details():
        selected_row = await serverDetailsTable.get_selected_row()
        if selected_row:
            server_details_rows[:] = [row for row in server_details_rows if row['id'] != selected_row['id']]
            serverDetailsTable.options['rowData'] = server_details_rows
            serverDetailsTable.update()
            ui.notify("Row removed successfully", type='positive')
        else:
            ui.notify("No row selected for removal", type='warning')

    def save_all_details():
        print("Server Details:")
        for row in server_details_rows:
            print(row)
        ui.notify("Data Saved", type='positive')

    with ui.dialog() as serverDetailsDialog:
        with bash_window("Add Server Detail", classes='w-full'):
            with ui.grid(columns=2).classes('gap-4'):
                os_type_select = ui.select(options=Os_type_option, label='OS Type').classes('pl-6 w-5/6')
                instance_type_select = ui.select(options=Instance_type_option, with_input=True, value="",
                                                 label='Instance Type').classes('pl-6 w-5/6')
                server_prefix_input = ui.input(label='Server Prefix').classes('pl-6 w-5/6')
                server_seq_num_input = ui.input(label='Server Sequence Number').classes('pl-6 w-5/6')
                quantity_input = ui.input(label='Quantity').classes('pl-6 w-5/6')
                subnet_info_input = ui.input(label='Subnet Information').classes('pl-6 w-5/6')

            with ui.row().classes('self-center place-items-center'):
                ui.button('Add', on_click=save_server_details, icon='add').classes('m-2')
                ui.button('Close', on_click=serverDetailsDialog.close, icon='close').classes('m-2')

    server_details_columns = [
        {'headerName': '', 'checkboxSelection': True, 'width': 50},  # Add checkbox selection
        {'headerName': 'OS Type', 'field': 'Os_type'},
        {'headerName': 'Instance Type', 'field': 'instance_type'},
        {'headerName': 'Server Prefix', 'field': 'server_prefix'},
        {'headerName': 'Server Sequence Number', 'field': 'Server_sequence_number'},
        {'headerName': 'Quantity', 'field': 'Quantity'},
        {'headerName': 'Subnet Information', 'field': 'Subnet_information'}
    ]

    with ui.card().classes('w-full'):
        with ui.row().classes('w-full'):
            serverDetailsTable = ui.aggrid({
                'defaultColDef': {'flex': 1},
                'columnDefs': server_details_columns,
                'rowData': server_details_rows,
                'rowSelection': 'single'
            }).classes('w-full')

        with ui.row().classes('self-center place-items-center'):
            ui.button('Add', on_click=serverDetailsDialog.open, icon='add').classes('m-2')
            ui.button('Edit', on_click=lambda: asyncio.create_task(edit_server_details()), icon='edit').classes('m-2')
            ui.button('Delete', on_click=lambda: asyncio.create_task(remove_server_details()), icon='delete').classes('m-2')
            ui.button('Save', on_click=save_all_details, icon='save').classes('m-2')
