from nicegui import ui
from jira import JIRA
import menu
from aws_details_tab import AwsDetailsForm
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Placeholder for getting environment variables
def get_env_var(key):
    # Implement this function to fetch environment variables
    return "Your_Value_Here"

userName = menu.getJsonVal("env_var", "JIRAUSER")
passWord = menu.getJsonVal("env_var", "JIRAPASS")
urlPath = menu.getJsonVal("env_var", "JIRAURL")
jiraOptions = {'server': urlPath, 'verify': False}
jira = JIRA(options=jiraOptions, basic_auth=(userName, passWord))
def GetProjectList(jira):
    jqlStr = menu.getJsonVal("env_var", "KICKOFF")
    all_issues = []
    start_at = 0
    max_results = 50  # Adjust this if needed
    while True:
        issues = jira.search_issues(jqlStr, startAt=start_at, maxResults=max_results)
        all_issues.extend(issues)
        if len(issues) < max_results:
            break  # Exit the loop if there are no more issues to fetch
        start_at += len(issues)

    issueList = [{'id': issue.key, 'summary': issue.fields.summary} for issue in all_issues]
    return issueList

aws_details_form_instance = AwsDetailsForm()
def setup_project_dropdown(jira, container):
    def on_project_select(event):
        nonlocal client_code_label
        selected_issue_key = event.value
        selected_issue = jira.issue(selected_issue_key)
        client_code = getattr(selected_issue.fields, 'customfield_45in567', 'Not Available')
        client_code_label.text = f"Client Code: {client_code}"

        selected_project_id = event.value
        aws_details_form_instance.update_with_project(selected_project_id)

    issueList = GetProjectList(jira)
    issue_options = [(issue['id'], f"{issue['id']} - {issue['summary']}") for issue in issueList]

    # Create the dropdown and label directly within the container
    issue_dropdown = container.select(label='Search Project', options=issue_options, with_input=True, on_change=on_project_select)
    client_code_label = container.label('Client Code: Not selected')







def display_project_details(project_id):
    # Logic to display details for the selected project
    pass

# This is assuming you are calling this function to set up the UI components
#setup_project_dropdown(jira)


