from tornado.web import RequestHandler
import json
import asyncio
import http_base_handler
import set_manager


class TestSetsHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['GET', 'POST']

    def get(self, *args, **kwargs):
        sets = set_manager.get_set_list()
        self.write_success_dict({'sets':sets})

    def post(self):
        try:
            content = json.loads(self.request.body)
            result = set_manager.add_set(content)
            if result:
                self.write_success_dict(result)
            else:
                self.write_bad_request("no name")
        except json.JSONDecodeError:
            self.write_bad_request('not a json string')


class SetHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['GET','DELETE','PATCH']

    def get(self, *args, **kwargs):
        set_index = int(args[0])
        result = set_manager.get_set_content(set_index)
        if result:
            self.write_success_dict(result)
        else:
            self.write_user_layer_error(1, "testset for %d no exist" % set_index)

    def delete(self, *args, **kwargs):
        set_index = int(args[0])
        result = set_manager.delete_set(set_index)
        if result:
            self.write_success_dict({})
        else:
            self.write_user_layer_error(1, "testset for %d no exist" % set_index)

    def patch(self, *args, **kwargs):
        try:
            content = json.loads(self.request.body)
            set_index = int(args[0])
            result = set_manager.patch_set(set_index, content)
            if result:
                self.write_success_dict({})
            else:
                self.write_user_layer_error(1, "testset for %d no exist" % set_index)
        except json.JSONDecodeError:
            self.write_bad_request('not a json string')



class SetInterfaceHandler(http_base_handler.BaseHandler):
    ALLOWED_METHODS = ['POST', 'PUT', 'DELETE']

    def post(self, *args, **kwargs):
        try:
            set_index = int(args[0])
            content = json.loads(self.request.body)
            result = set_manager.post_interface(set_index, content)
            if result:
                self.write_success_dict({})
            else:
                self.write_user_layer_error(1, "testset for %d no exist" % set_index)
        except json.JSONDecodeError:
            self.write_bad_request('not a json string')

    def put(self, *args, **kwargs):
        try:
            set_index = int(args[0])
            interface_index = int(args[1])

            content = json.loads(self.request.body)
            result = set_manager.put_or_delete_interface(set_index, interface_index, content)
            if result:
                self.write_success_dict({})
            else:
                self.write_user_layer_error(1,"testset for %d no exist or interface not exist"
                                            % set_index)
        except json.JSONDecodeError:
            self.write_bad_request('not a json string')
        except ValueError:
            self.write_bad_request('need interface index')

    def delete(self, *args, **kwargs):
        try:
            set_index = int(args[0])
            interface_index = int(args[1])
            result = set_manager.put_or_delete_interface(set_index, interface_index, None, 1)
            if result:
                self.write_success_dict({})
            else:
                self.write_user_layer_error(1, "testset for %d no exist or interface not exist"
                                            % set_index)
        except json.JSONDecodeError:
            self.write_bad_request('not a json string')
        except ValueError:
            self.write_bad_request('need interface index')


