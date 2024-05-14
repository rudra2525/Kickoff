from nicegui import events, ui
import myDbConnection
import menu
import time

def setup_server_details():
    Os_type_option = myDbConnection.query_os_type()
    Instance_type_option = myDbConnection.query_allowed_values('AWS_INSTANCE')

    adGrprows = []

    AdGrpTableCol = [
        {'name': 'Os_type', 'label': 'OS Type', 'field': 'Os_type', 'required': True, 'align': 'left', 'width': '20%', 'headerStyle': 'min-width: 25px'},
        {'name': 'instance_type', 'label': 'Instance Type', 'field': 'instance_type', 'required': True, 'align': 'left', 'width': '20%', 'headerStyle': 'min-width: 25px'},
        {'name': 'server_prefix', 'label': 'Server Prefix', 'field': 'server_prefix', 'required': True, 'align': 'left', 'width': '20%', 'headerStyle': 'min-width: 25px'},
        {'name': 'Server_sequence_number', 'label': 'Server Sequence Number', 'field': 'Server_sequence_number', 'required': True, 'align': 'left', 'width': '20%', 'headerStyle': 'min-width: 25px'},
        {'name': 'Quantity', 'label': 'Quantity', 'field': 'Quantity', 'required': True, 'align': 'left', 'width': '20%', 'headerStyle': 'min-width: 25px'},
        {'name': 'Subnet_information', 'label': 'Subnet Information', 'field': 'Subnet_information', 'required': True, 'align': 'left', 'width': '20%', 'headerStyle': 'min-width: 25px'},
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


    with ui.card().classes('w-full'):
            with ui.table(columns=AdGrpTableCol, rows=adGrprows).classes('w-full') as aGrptable:
                aGrptable.add_slot(
                    "body",
                    r"""
                    <q-tr :props="props">
                        <q-td key="Os_type" :props="props" class="w-8 ellipsis">
                            {{ props.row.Os_type }}
                        </q-td>
                        <q-td key="instance_type" :props="props" class="w-8 ellipsis">
                            {{ props.row.instance_type }}
                        </q-td>
                        <q-td key="server_prefix" :props="props" class="w-8 ellipsis">
                            {{ props.row.server_prefix }}
                        </q-td>
                        <q-td key="Server_sequence_number" :props="props" class="w-8 ellipsis">
                            {{ props.row.Server_sequence_number }}
                        </q-td>
                        <q-td key="Quantity" :props="props" class="w-8 ellipsis">
                            {{ props.row.Quantity }}
                        </q-td>
                        <q-td key="Subnet_information" :props="props" class="w-8 ellipsis">
                            {{ props.row.Subnet_information }}
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
                            u_env_type = ui.select(options=Os_type_option, with_input=True, value="", label='OS Type').classes(f"w-full").props('rounded outlined dense')
                        with aGrptable.cell():
                            u_aws_acc = menu.form_select(Instance_type_option, 'Instance Type', "", "w-full").props('rounded outlined dense')
                        with aGrptable.cell():
                            u_aws_reg = ui.input(label="Server Prefix", placeholder="Enter Server Prefix").classes('w-full').props('rounded outlined dense''clearable')
                        with aGrptable.cell():
                            ui.button(on_click=lambda: (aGrptable.add_rows({'id': time.time(), 'Environment_type': u_env_type.value,'aws_account': u_aws_acc.value, "aws_region": u_aws_reg.value}),
                                u_env_type.set_value(None),
                                u_aws_acc.set_value(None),
                                u_aws_reg.set_value(None)
                            ), icon='add')

                    aGrptable.on("delete", deleteGrp)
            ui.button('Save', on_click=print_table_data, icon='save')
