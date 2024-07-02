from nicegui import app, ui, client
import server_detailsDlg
from website.demo import section_window
import myDbConnection
import menu


def setup_serverDetail(ProjDetail):
    global gEnv_Name
    gEnv_Name = ""
    aws_details_rows = app.storage.aws_details
    aws_details_columns = [
        {'headerName': '', 'checkboxSelection': True, 'width': 50},
        {'headerName': 'Environment Type', 'field': 'environment_type'},
        {'headerName': 'Aws Account', 'field': 'aws_acc'},
        {'headerName': 'Aws Region', 'field': 'aws_region'}
    ]

    with section_window("AWS Details", classes='w-full'):
        with ui.row().classes("w-full"):
            with ui.card().classes('w-full'):
                with ui.row().classes('w-full'):
                    awsDetailsTable = ui.aggrid({
                        'defaultColDef': {'flex': 1},
                        'columnDefs': aws_details_columns,
                        'rowData': aws_details_rows,
                        'rowSelection': 'single'
                    }).classes('w-full')

    server_details_columns = [
        {'headerName': '', 'checkboxSelection': True, 'width': 50},
        {'headerName': 'Environment', 'field': 'environment'},
        {'headerName': 'OS Type', 'field': 'Os_type'},
        {'headerName': 'Instance Type', 'field': 'instance_type'},
        {'headerName': 'Server Prefix', 'field': 'server_prefix'},
        {'headerName': 'Server Sequence Number', 'field': 'Server_sequence_number'},
        {'headerName': 'Quantity', 'field': 'Quantity'},
        {'headerName': 'Subnet Information', 'field': 'Subnet_information'}
    ]

    server_details_rows = app.storage.server_details

    def add_serverDetail(SeverDet):
        server_details_rows.extend(SeverDet)
        app.storage.server_details = server_details_rows
        serverDetailsTable.options['rowData'] = sorted(server_details_rows)
        ui.notify("Server Detail Added Successfully", type='positive')
        serverDetailsTable.update()
        serverDetailsTable.call_api_method('setQuickFilter', gEnv_Name)

    def edit_serverDetail(SeverDet):
        for rowData in SeverDet:
            if rowData["EnvName"] == SeverDet[0]["EnvName"] and rowData["Software"] == SeverDet[0]["Software"]:
                server_details_rows.remove(rowData)

        server_details_rows.extend(SeverDet)
        serverDetailsTable.options['rowData'] = sorted(server_details_rows, key=lambda data: data["EnvName"])
        ui.notify("Server Detail Updated Successfully", type='positive')
        serverDetailsTable.update()
        serverDetailsTable.call_api_method('setQuickFilter', gEnv_Name)

    async def NewServerDetailDlg():
        selected_row = await awsDetailsTable.get_selected_row()
        if selected_row:
            server_detailsDlg.serverDetail(selected_row['environment_type'], "A", add_serverDetail, [])
        else:
            ui.notify("No AWS Detail row selected", type='warning')

    async def EditServerDetailDlg():
        if gEnv_Name:
            CustSpecSelect = await serverDetailsTable.get_selected_row()
            if CustSpecSelect:
                server_detailsDlg.serverDetail(gEnv_Name, "U", edit_serverDetail, CustSpecSelect)
            else:
                ui.notify("Server Detail is not Selected", type='negative')
        else:
            ui.notify("Environment is not Selected", type='negative')

    async def delServerDetail():
        row = await serverDetailsTable.get_selected_row()

        if row is None:
            ui.notify("No Row selected")
        else:
            server_details_rows.remove(row)
            app.storage.server_details = server_details_rows
            serverDetailsTable.options['rowData'] = sorted(server_details_rows, key=lambda data: data["EnvName"])
            serverDetailsTable.update()
            serverDetailsTable.call_api_method('setQuickFilter', gEnv_Name)  ## Filter after del
            ui.notify("Custom Specs Information Removed Successfully", type='positive')

    def save_server_info():
        app.storage.server_details = server_details_rows
        ui.notify("Server Details Saved", type='positive')

    with ui.card().classes('w-full mt-4'):
        with ui.row().classes('w-full'):
            serverDetailsTable = ui.aggrid({
                'defaultColDef': {'flex': 1},
                'columnDefs': server_details_columns,
                'rowData': server_details_rows,
                'rowSelection': 'single'
            }).classes('w-full')
            ui.button(icon='add', on_click=NewServerDetailDlg)
            ui.button(icon='edit', on_click=EditServerDetailDlg)
            ui.button(icon='delete', on_click=delServerDetail)
            ui.button(icon='save', on_click=save_server_info)
