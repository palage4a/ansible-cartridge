#!/usr/bin/env python

from ansible.module_utils.helpers import Helpers as helpers

argument_spec = {
    'module_hostvars': {'required': True, 'type': 'dict'},
    'play_hosts': {'required': True, 'type': 'list'},
}


def get_one_not_expelled_instance(params):
    module_hostvars = params['module_hostvars']
    play_hosts = params['play_hosts']

    not_expelled_instance_name = None

    for instance_name in play_hosts:
        instance_vars = module_hostvars[instance_name]
        if helpers.is_expelled(instance_vars) or helpers.is_stateboard(instance_vars):
            continue

        not_expelled_instance_name = instance_name
        break

    if not_expelled_instance_name is None:
        errmsg = "Not found any instance that is not expelled and is not a stateboard"
        return helpers.ModuleRes(failed=True, msg=errmsg)

    instance_info = module_hostvars[not_expelled_instance_name]['instance_info']

    return helpers.ModuleRes(changed=False, fact={
        'name': not_expelled_instance_name,
        'console_sock': instance_info['console_sock'],
    })


if __name__ == '__main__':
    helpers.execute_module(argument_spec, get_one_not_expelled_instance)