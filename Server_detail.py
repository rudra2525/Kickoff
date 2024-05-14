from nicegui import events, ui
import myDbConnection
import menu
import time

def setup_server_details():
    # Fetch data from database
    Os_type_option = myDbConnection.query_os_type()
    Instance_type_option = myDbConnection.query_allowed_values('AWS_INSTANCE')

    adGrprows = []

    AdGrpTableCol = [
        {'name': 'Os_type', 'label': 'OS Type', 'field': 'Os_type', 'required': True, 'align': 'left', 'width': '20%'},
        {'name': 'instance_type', 'label': 'Instance Type', 'field': 'instance_type', 'required': True, 'align': 'left', 'width': '20%'},
        {'name': 'server_prefix', 'label': 'Server Prefix', 'field': 'server_prefix', 'required': True, 'align': 'left', 'width': '20%'},
        {'name': 'Server_sequence_number', 'label': 'Server Sequence Number', 'field': 'Server_sequence_number', 'required': True, 'align': 'left', 'width': '20%'},
        {'name': 'Quantity', 'label': 'Quantity', 'field': 'Quantity', 'required': True, 'align': 'left', 'width': '20%'},
        {'name': 'Subnet_information', 'label': 'Subnet Information', 'field': 'Subnet_information', 'required': True, 'align': 'left', 'width': '20%'},
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
                        os_type_select = ui.select(options=Os_type_option, label='OS Type')
                    with aGrptable.cell():
                        instance_type_select = ui.select(options=Instance_type_option, label='Instance Type')
                    with aGrptable.cell():
                        server_prefix_input = ui.input(label='Server Prefix')
                    with aGrptable.cell():
                        server_seq_num_input = ui.input(label='Server Sequence Number')
                    with aGrptable.cell():
                        quantity_input = ui.input(label='Quantity')
                    with aGrptable.cell():
                        subnet_info_input = ui.input(label='Subnet Information')
                    with aGrptable.cell():
                        ui.button(on_click=lambda: (aGrptable.add_rows({'id': time.time(), 'Os_type': os_type_select.value, 'instance_type': instance_type_select.value, 'server_prefix': server_prefix_input.value, 'Server_sequence_number': server_seq_num_input.value, 'Quantity': quantity_input.value, 'Subnet_information': subnet_info_input.value}),
                                  os_type_select.set_value(None),
                                  instance_type_select.set_value(None),
                                  server_prefix_input.set_value(None),
                                  server_seq_num_input.set_value(None),
                                  quantity_input.set_value(None),
                                  subnet_info_input.set_value(None)
                                                    ), icon='add')
                aGrptable.on("delete", deleteGrp)

        ui.button('Save', on_click=print_table_data, icon='save')
