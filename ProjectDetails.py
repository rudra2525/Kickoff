from nicegui import ui

class ProjectDetails:
    ui.label('Project Details').classes('text-h4')
    with ui.card().classes(''):
        with ui.grid(columns = 4):
            ui.input(label ='Project Name')
            ui.input(label='Jira Key')
            ui.input(label='Project Type')
            ui.input(label='Platform')
            ui.input(label='Location')
            ui.input(label='Client Code')
            ui.input(label='Tech Owner')
            ui.input(label='Tech Lead')
