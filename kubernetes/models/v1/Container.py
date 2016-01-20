from kubernetes.models.v1.BaseModel import BaseModel


class Container(BaseModel):
    def __init__(self, name=None, image=None, model=None):
        BaseModel.__init__(self)
        if model is not None:
            assert isinstance(model, dict)
            self.model = model
        else:
            if name is None or image is None:
                raise SyntaxError
            self.model = {
                "name": name,
                "image": image,
                "imagePullPolicy": 'IfNotPresent',
                "privileged": False,
                "hostNetwork": False,
                "resources": {
                    "requests": {
                        "cpu": 0.1,
                        "memory": "32M"
                    }
                }
            }

    def add_port(self, container_port, host_port, protocol='TCP', name=None):
        if container_port > 0 and host_port > 0:
            if name is None:
                name = 'port{portnum}'.format(portnum=str(host_port))
            if 'ports' not in self.model.keys():
                self.model['ports'] = []
            self.model['ports'].append({
                "containerPort": int(container_port),
                "hostPort": int(host_port),
                "protocol": protocol,
                "name": name
            })
        else:
            raise SyntaxError('container_port and host_port should be integers.')
        return self

    def add_env(self, name=None, value=None):
        if name is None or value is None:
            raise SyntaxError('name and value should be strings.')
        else:
            if 'env' not in self.model.keys():
                self.model['env'] = []
            self.model['env'].append({"name": name, "value": value})
        return self

    def add_volume_mount(self, name=None, read_only=False, mount_path=None):
        if name is None or mount_path is None:
            raise SyntaxError('name and mount_path should be strings.')
        else:
            if 'volumeMounts' not in self.model.keys():
                self.model['volumeMounts'] = []
            self.model['volumeMounts'].append({
                "name": name,
                "readOnly": read_only,
                "mountPath": mount_path
            })
        return self

    def set_arguments(self, args=None):
        if args is None:
            args = []
        else:
            if not isinstance(args, list):
                raise SyntaxError('args should be a list.')
        if 'args' not in self.model.keys():
            self.model['args'] = []
        self.model['args'] = args
        return self

    def set_command(self, cmd=None):
        if cmd is None:
            cmd = []
        else:
            if not isinstance(cmd, list):
                raise SyntaxError('cmd should be a list.')
        if 'command' not in self.model.keys():
            self.model['command'] = []
        self.model['command'] = cmd
        return self

    def set_host_network(self, mode=True):
        if not isinstance(mode, bool):
            raise SyntaxError('mode should be True or False')
        self.model['hostNetwork'] = mode
        return self

    def set_image(self, image=None):
        if image is None:
            raise SyntaxError('image should be a string.')
        else:
            self.model['image'] = image
        return self

    def set_name(self, name=None):
        if name is None:
            raise SyntaxError('name should be a string.')
        else:
            self.model['name'] = name
        return self

    def set_pull_policy(self, policy='IfNotPresent'):
        if not isinstance(policy, str):
            raise SyntaxError('Policy should be one of: Always, Never, IfNotPresent')
        if policy in ['Always', 'Never', 'IfNotPresent']:
            self.model['imagePullPolicy'] = policy
        else:
            raise SyntaxError
        return self

    def set_privileged(self, mode=True):
        if not isinstance(mode, bool):
            raise SyntaxError('mode should be True or False')
        self.model['privileged'] = mode
        return self

    def set_requested_resources(self, cpu=0.1, mem='32M'):
        if not isinstance(cpu, float) or not isinstance(mem, str):
            raise SyntaxError('cpu should be a positive float and mem should be a string like 32M, 1G')
        self.model['resources']['requests']['cpu'] = cpu
        self.model['resources']['requests']['memory'] = mem
        return self

    def set_limit_resources(self, cpu=0.1, mem='32M'):
        if not isinstance(cpu, float) or not isinstance(mem, str):
            raise SyntaxError('cpu should be a positive float and mem should be a string like 32M, 1G')
        assert isinstance(self.model['resources'], dict)
        if 'limits' not in self.model['resources'].keys():
            self.model['resources']['limits'] = dict()
        self.model['resources']['limits']['cpu'] = cpu
        self.model['resources']['limits']['memory'] = mem
        return self
