import os
import re
import unittest

import yaml


# This tests protects against inattentive people, who do not completely change the variables list

class TestFacts(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        role_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

        self.defaults_file = os.path.join(role_dir, 'defaults', 'main.yml')
        with open(self.defaults_file, 'r') as f:
            try:
                self.defaults = yaml.safe_load(f)
            except yaml.YAMLError as e:
                self.fail("Impossible to parse 'defaults/main.yml': %s" % e)

        self.set_instance_facts_file = os.path.join(role_dir, 'tasks', 'set_instance_facts.yml')
        with open(self.set_instance_facts_file, 'r') as f:
            try:
                self.set_instance_facts = yaml.safe_load(f)
            except yaml.YAMLError as e:
                self.fail("Impossible to parse 'tasks/set_instance_facts.yml': %s" % e)

        self.doc_facts_file = os.path.join(role_dir, 'doc', 'variables.md')
        with open(self.doc_facts_file, 'r') as f:
            text = f.read()
            self.doc_facts = re.findall(r'\n[*-][^`]*`([^`]+)`', text)

        self.not_user_facts = [
            # Role defaults
            'cartridge_role_scenarios',
            'cartridge_cached_fact_names_by_target',
            # Cross-step facts
            'delivered_package_path',
            'control_instance',
            'temporary_files',
            'needs_restart',
            'cluster_disabled_instances',
            'inventory_disabled_instances',
            'alive_not_expelled_instance',
            'instance_backup_files',
            'backup_archive_path',
            'fetched_backup_archive_path',
            'backup_files_from_machine',
            # Temp facts
            'cached_facts',
            'facts_for_machines_res',
            'single_instances_for_each_machine',
            'instances_from_same_machine',
        ]

    # If someone added a variable to defaults, but forgot to set it in 'set_instance_facts' step
    def test_set_instance_facts(self):
        default_names = list(self.defaults.keys())
        set_instance_facts_name = list(self.set_instance_facts[0]['set_fact']['role_facts'].keys())

        self.assertEqual(
            sorted(default_names), sorted(set_instance_facts_name + self.not_user_facts),
            'List of facts in defaults and in "set_instance_fact" step is different',
        )

    # If someone added a variable to defaults, but forgot to add it to doc
    def test_doc_facts(self):
        default_names = list(self.defaults.keys())

        self.assertEqual(
            sorted(default_names), sorted(self.doc_facts + self.not_user_facts),
            'List of facts in defaults and in documentation is different',
        )