#  Copyright 2026 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

# FIXME: THIS WHOLE FILE CAN BE DELETED AFTER WE UPDATE ARIADNE-CODEGEN TO > 0.18.0
import ast
import sys
from typing import Optional

import click
import ariadne_codegen.client_generators.custom_operation
from ariadne_codegen.plugins.manager import PluginManager
from graphql import assert_valid_schema


class ZBPatchedPluginManager(PluginManager):
    def generate_custom_module(self, module: ast.Module) -> ast.Module:
        return self._apply_plugins_on_object("generate_custom_module", module)

    def generate_custom_method(self, method_def: ast.FunctionDef) -> ast.FunctionDef:
        return self._apply_plugins_on_object("generate_custom_method", method_def)


class ZBPatchedCustomOperationGenerator(
    ariadne_codegen.client_generators.custom_operation.CustomOperationGenerator
):
    plugin_manager: ZBPatchedPluginManager

    def _generate_method(
        self,
        operation_name: str,
        operation_args,
        final_type,
        description: Optional[str] = None,
    ) -> ast.FunctionDef:
        return self.plugin_manager.generate_custom_method(
            super()._generate_method(
                operation_name,
                operation_args,
                final_type,
                description,
            )
        )

    def generate(self) -> ast.Module:
        return self.plugin_manager.generate_custom_module(super().generate())


ariadne_codegen.client_generators.custom_operation.CustomOperationGenerator = (
    ZBPatchedCustomOperationGenerator
)


from ariadne_codegen.client_generators.package import get_package_generator
from ariadne_codegen.config import (
    get_client_settings,
    get_config_dict,
    get_graphql_schema_settings,
)
from ariadne_codegen.graphql_schema_generators.schema import (
    generate_graphql_schema_graphql_file,
    generate_graphql_schema_python_file,
)
from ariadne_codegen.plugins.explorer import get_plugins_types
from ariadne_codegen.plugins.base import Plugin
from ariadne_codegen.schema import (
    add_mixin_directive_to_schema,
    filter_fragments_definitions,
    filter_operations_definitions,
    get_graphql_queries,
    get_graphql_schema_from_path,
    get_graphql_schema_from_url,
)
from ariadne_codegen.settings import Strategy, get_validation_rule

Plugin.generate_custom_method = lambda self, method: method
Plugin.generate_custom_module = lambda self, module: module


@click.command()
@click.version_option()
@click.option("--config", default=None, help="Path to custom configuration file.")
@click.argument(
    "strategy",
    default=Strategy.CLIENT.value,
    type=click.Choice([e.value for e in Strategy]),
    required=False,
)
def main(strategy=Strategy.CLIENT.value, config=None):
    config_dict = get_config_dict(config)
    if strategy == Strategy.CLIENT:
        client(config_dict)

    if strategy == Strategy.GRAPHQL_SCHEMA:
        graphql_schema(config_dict)


def client(config_dict):
    settings = get_client_settings(config_dict)

    if settings.schema_path:
        schema = get_graphql_schema_from_path(settings.schema_path)
    else:
        schema = get_graphql_schema_from_url(
            url=settings.remote_schema_url,
            headers=settings.remote_schema_headers,
            verify_ssl=settings.remote_schema_verify_ssl,
            timeout=settings.remote_schema_timeout,
            introspection_settings=settings.introspection_settings,
        )

    plugin_manager = ZBPatchedPluginManager(
        schema=schema,
        config_dict=config_dict,
        plugins_types=get_plugins_types(settings.plugins),
    )
    schema = add_mixin_directive_to_schema(schema)
    schema = plugin_manager.process_schema(schema)
    assert_valid_schema(schema)

    fragments = []
    queries = []
    if settings.queries_path:
        definitions = get_graphql_queries(
            settings.queries_path,
            schema,
            [get_validation_rule(e) for e in settings.skip_validation_rules],
        )
        queries = filter_operations_definitions(definitions)
        fragments = filter_fragments_definitions(definitions)

    sys.stdout.write(settings.used_settings_message)

    package_generator = get_package_generator(
        schema=schema,
        fragments=fragments,
        settings=settings,
        plugin_manager=plugin_manager,
    )
    for query in queries:
        package_generator.add_operation(query)
    generated_files = package_generator.generate()

    sys.stdout.write("\nGenerated files:\n  " + "\n  ".join(generated_files) + "\n")


def graphql_schema(config_dict):
    settings = get_graphql_schema_settings(config_dict)

    schema = (
        get_graphql_schema_from_path(settings.schema_path)
        if settings.schema_path
        else get_graphql_schema_from_url(
            url=settings.remote_schema_url,
            headers=settings.remote_schema_headers,
            verify_ssl=settings.remote_schema_verify_ssl,
            timeout=settings.remote_schema_timeout,
            introspection_settings=settings.introspection_settings,
        )
    )
    plugin_manager = ZBPatchedPluginManager(
        schema=schema,
        config_dict=config_dict,
        plugins_types=get_plugins_types(settings.plugins),
    )
    schema = plugin_manager.process_schema(schema)
    assert_valid_schema(schema)

    sys.stdout.write(settings.used_settings_message)

    if settings.target_file_format == "py":
        generate_graphql_schema_python_file(
            schema=schema,
            target_file_path=settings.target_file_path,
            type_map_name=settings.type_map_variable_name,
            schema_variable_name=settings.schema_variable_name,
        )
    else:
        generate_graphql_schema_graphql_file(
            schema=schema,
            target_file_path=settings.target_file_path,
        )


if __name__ == "__main__":
    import os
    print(os.getcwd())
    print(
        "TEMPORARY PATCHED VERSION IN USE. check if ariadne-codegen has been released > 0.10.8"
    )
    main()
