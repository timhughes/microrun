
from openapi.spec import op
from openapi.spec.path import ApiPath


class Index(ApiPath):
    """
    ---
    summary: Index page data
    description: Index page description
    tags:
        - name: Index
          description: Simple description

    """

    @op()
    async def get(self):
        """
        ---
        summary: Get Index
        description: Returns the data for the index page
        responses:
            200:
                description: Index page
        """
        return self.json_response({})


class Services(ApiPath):
    """
    ---
    summary: Services
    description: List of services
    tags:
        - name: Index
          description: Simple description
    """

    @op()
    async def get(self):
        """
        ---
        summary: Services list
        description: Gets a list of services
        responses:
            200:
                description: What you want
        """

        msm = self.request.app['msm']
        service_names = msm.services_list
        return self.json_response(service_names)


    @op()
    async def post(self):
        """
        ---
        summary: Services list
        description: Gets a list of services
        responses:
            200:
                description: What you want
        """

        # TODO: Get the action from the post and call the action against the service
        # Can we have multiple urls go to the same handler class?
        # Do all the list, start, stop, status
        # eg:
        #    if 'action' in request.match_info.keys():
        #        action = request.match_info['action']
        #        if action = 'stop':
        #             mvm.stop_service(name)
        #

        return self.json_response({'result': 'success'})




