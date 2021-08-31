import os
import json

class MockQuicksightClient:
    """Very basic mock of the Boto3 Quicksight client, only mocks the functionality required for this particular lambda"""

    # def __init__(self, test_directory):
    #     self.test_directory = test_directory
    def list_user_groups(self, UserName, AwsAccountId, Namespace):
        if not len(AwsAccountId) == 12:
            raise ParamValidationError(
                f"Invalid length for parameter AwsAccountId, value: {len(AwsAccountId)}, valid min length: 12"
            )
        with open('json/group_membership.json', "r+") as f:
            membership_json = json.load(f)
            users_list = membership_json['groups']
            # sorry for all the loops... 
            # for each group in the groups_membership file
            # we loop through each member checking for our username
            # if the user is in the group...
            # then loop through the groups_list file objects matching the group names
            # to return the list of group objects which we are mocking
            group_membership_list = []
            with open('json/groups_list.json', "r+") as fg:
                groups_json = json.load(fg)['item']
                for group in users_list:
                    users_in_group = users_list[group]
                    for user in users_in_group:
                        if user['MemberName'] == UserName:
                            for group_json in groups_json:
                                if group_json['GroupName'] == group:
                                    group_membership_list.append(group_json)

            return self.build_response("GroupList", group_membership_list)

    def create_group_membership(self, MemberName, GroupName, AwsAccountId, Namespace):
        if not len(AwsAccountId) == 12:
            raise ParamValidationError(
                f"Invalid length for parameter AwsAccountId, value: {len(AwsAccountId)}, valid min length: 12"
            )
        with open('json/group_membership.json', "r+") as f:
            membership_json = json.load(f)
            users_list = membership_json['groups'][GroupName.lower()]
            duplicate = False
            for user in users_list:
                if user['MemberName'] == MemberName:
                    duplicate = True
            if not duplicate:
                users_list.append({"Arn": f"arn/{MemberName}", "MemberName": MemberName})
            with open('json/group_membership.json', "wt") as fp: 
                membership_json['groups'][GroupName] = users_list

                json.dump(membership_json, fp)
            return self.build_response("hello", "hello")


    def delete_group_membership(self, MemberName, GroupName, AwsAccountId, Namespace):
        if not len(AwsAccountId) == 12:
            raise ParamValidationError(
                f"Invalid length for parameter AwsAccountId, value: {len(AwsAccountId)}, valid min length: 12"
            )
        with open('json/group_membership.json', "r+") as f:
            membership_json = json.load(f)
            users_list = membership_json['groups'][GroupName]
            
            users_list.remove({"Arn": f"arn/{MemberName}", "MemberName": MemberName})
            
            with open('json/group_membership.json', "wt") as fp: 
                membership_json['groups'][GroupName] = users_list

                json.dump(membership_json, fp)
            return self.build_response("hello", "hello")
       

    def list_group_memberships(self, GroupName, AwsAccountId, MaxResults=100, NextToken=0, Namespace="default"):
        if not len(AwsAccountId) == 12:
            raise ParamValidationError(
                f"Invalid length for parameter AwsAccountId, value: {len(AwsAccountId)}, valid min length: 12"
            )
        with open('json/group_membership.json') as f:
            users_list = json.load(f)['groups'][GroupName]

            return self.build_response("GroupMemberList", users_list)

    def list_users(self, AwsAccountId, Namespace):
        if not len(AwsAccountId) == 12:
            raise ParamValidationError(
                f"Invalid length for parameter AwsAccountId, value: {len(AwsAccountId)}, valid min length: 12"
            )
        with open('json/users_list.json') as f:
            users_list = json.load(f)['item']
            return self.build_response("UserList", users_list)


    def list_groups(self, AwsAccountId, Namespace, MaxResults=100, NextToken="0/"):
        if not len(AwsAccountId) == 12:
            raise ParamValidationError(
                f"Invalid length for parameter AwsAccountId, value: {len(AwsAccountId)}, valid min length: 12"
            )
        with open('json/groups_list.json') as f:
            
            next_token = int(NextToken.split("/")[0])
            groups_list = json.load(f)['item']
            
            paginated_groups_list = groups_list[next_token: next_token+MaxResults]
            new_next_token = f"{next_token + MaxResults}/hello"

            if len(groups_list) <= next_token + MaxResults:
                return self.build_response("GroupList", paginated_groups_list)
            return self.build_response("GroupList", paginated_groups_list, new_next_token)


    def list_dashboards(self, AwsAccountId):
        if not len(AwsAccountId) == 12:
            raise ParamValidationError(
                f"Invalid length for parameter AwsAccountId, value: {len(AwsAccountId)}, valid min length: 12"
            )
        with open('json/dashboards.json') as f:
            dashboard_list = json.load(f)['dashboards']
            return self.build_response("DashboardSummaryList", dashboard_list)


    #  The below method is a remnant from a working `create_user` mock so could be useful in the future
    
#     def get_list_added_user(self, UserName, Email, UserRole, IdentityType):
#         with open('json/users_list.json') as f:
#             users_list = json.load(f)['item']
# # This doesn't error, it just overwrites if email already exists - Dom 
#             for user in users_list:
#                 if user["Email"] == Email:
#                     raise Exception
            
#             number = len(users_list) + 1
#             user = {
#                     "Arn":f"Test_User_{number}",
#                     "UserName": UserName,
#                     "Email": Email,
#                     "Role":UserRole,
#                     "IdentityType":IdentityType,
#                     "Active":True,
#                     "PrincipalId":f"federated/iam/Test_ID:{Email}"
#                 }
#             users_list.append(user)
#             return users_list

    def get_dashboard_embed_url(
        self,
        AwsAccountId,
        DashboardId,
        IdentityType,
        SessionLifetimeInMinutes,
        UndoRedoDisabled,
        ResetDisabled,
        UserArn,
    ):
        if not len(AwsAccountId) == 12:
            raise ParamValidationError(
                f"Invalid length for parameter AwsAccountId, value: {len(AwsAccountId)}, valid min length: 12"
            )
        with open('json/embed_url_list.json') as f:
            dashboards = json.load(f)['dashboards']
            for dashboard in dashboards:
                if dashboard["dashboard_id"] == DashboardId:
                    region = dashboard['arn'].split(":")
                    embed_url = f'''https://{region}.quicksight.aws.amazon.com/embed/embed_code/dashboards/{DashboardId}?code=EMBED_CODE
                    identityprovider={IdentityType.lower()}&isauthcode=true&undoRedoDisabled={UndoRedoDisabled}&resetDisabled={ResetDisabled}'''

                    return self.build_response("EmbedUrl", embed_url)
  
    @staticmethod
    def build_response(item_name, item, next_token=None):
        return {
                "ResponseMetadata":{
                "RequestId":"Test_Request_ID",
                "HTTPStatusCode":200,
                "HTTPHeaders":{
                    "date":"Test_Date",
                    "content-type":"application/json",
                    "content-length":"Test",
                    "connection":"keep-alive",
                    "x-amzn-requestid":"Test_Request_ID"
                },
                "RetryAttempts":0
                },
                "Status":200,
                item_name: item,
                "NextToken": next_token,
                "RequestId":"Test_Request_ID"
            }

class ParamValidationError(Exception):
    pass