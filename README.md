# boto3-mock-aws-quicksight
A library to mock the Boto3 methods for AWS QuickSight. `Moto haven't done it as of now :)`

This library mocks some of the Quicksight Boto3 methods for testing purposes. I have used json files as objects to replicate what must be going on in the quicksight api.

## Available methods
A list of the available quicksight boto3 methods can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html)

The following are currently mocked in this library:

`create_group_membership`

`delete_group_membership`

`get_dashboard_embed_url`

`list_groups`

`list_group_memberships`

`list_users`

`list_user_groups`

`list_dashboards`
