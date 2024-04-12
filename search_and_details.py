from nicegui import ui
from jira import JIRA
import menu
import urllib3
from aws_details_tab import AwsDetailsForm
from ProjectDet import ProjecDetail

aws_details_form = AwsDetailsForm()

# Disable warnings from unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Fetch necessary credentials and URLs from your environment variables or configuration
userName = menu.getJsonVal("env_var", "JIRAUSER")
passWord = menu.getJsonVal("env_var", "JIRAPASS")
urlPath = menu.getJsonVal("env_var", "JIRAURL")

# Configure and initialize JIRA client
jiraOptions = {'server': urlPath, 'verify': False}
jira = JIRA(options=jiraOptions, basic_auth=(userName, passWord))


def GetProjectList(jira):
    # Fetch the list of projects from JIRA based on a query
    jqlStr = menu.getJsonVal("env_var", "KICKOFF")
    all_issues = []
    start_at = 0
    max_results = 50

    # Iterate through all available issues in batches
    while True:
        issues = jira.search_issues(jqlStr, startAt=start_at, maxResults=max_results)
        all_issues.extend(issues)
        if len(issues) < max_results:
            break
        start_at += len(issues)

    # Compile a list of dictionaries with issue IDs and summaries
    issueList = [{'id': issue.key, 'summary': issue.fields.summary} for issue in all_issues]
    return issueList


def setup_project_dropdown(jira, container, aws_details_form_instance):
    # Callback function for handling project selection changes
    def on_project_select(event):
        selected_issue_key = event.value
        selected_issue = jira.issue(selected_issue_key)

        # Fetch the client code from the selected issue using its custom field ID
        client_code = getattr(selected_issue.fields, 'customfield_45567', 'Not Available')
        aws_details_form_instance.setup_aws_account_dropdown(client_code)

        # Update the text of the client code label to display the fetched client code
        #client_code_label.text = f"Client Code: {client_code}"

        proj_details = {
            "summary": selected_issue.fields.summary,
            "jirakey": selected_issue.key,
            # You need to replace 'customfield_xxxx' with the actual field ID in your JIRA setup.
            "Projecttype": getattr(selected_issue.fields, 'customfield_17322', 'Not Available'),
            "platform": getattr(selected_issue.fields, 'customfield_xxxx', 'Not Available'),
            "Location": getattr(selected_issue.fields, 'customfield_41320', 'Not Available'),
            "ClientCode": getattr(selected_issue.fields, 'customfield_45567', 'Not Available'),
            "Bustechowner": getattr(selected_issue.fields, 'customfield_55222', 'Not Available'),
            "Techlead": getattr(selected_issue.fields, 'customfield_59620', 'Not Available'),
            "DBAlead": getattr(selected_issue.fields, 'customfield_xxxx', 'Not Available'),
            "eEnvironment": getattr(selected_issue.fields, 'customfield_xxxx', 'Not Available'),
            "Objective": getattr(selected_issue.fields, 'customfield_xxxx', 'Not Available'),

        }

        ProjecDetail(proj_details)

    # Fetch the list of projects/issues to populate the dropdown options
    issueList = GetProjectList(jira)
    issue_options = [(issue['id'], f"{issue['id']} - {issue['summary']}") for issue in issueList]
    issue_dropdown = container.select(label='Search Project', options=issue_options, with_input=True, on_change=on_project_select).style('width: 256px;')
    #client_code_label = container.label('Client Code: Not selected')



