"""
Author: Giordon Stark <gstark@cern.ch>
Copyright © 2025 Giordon Stark. All rights reserved.
Unauthorized copying, redistribution, or use of this script, in whole or in part, is strictly prohibited.
"""
from __future__ import annotations

import logging
from typing import Annotated

import itkdb
import typer
from module_qc_database_tools.db import prod
from rich import print
from rich.logging import RichHandler
from rich.tree import Tree

log = logging.getLogger(__name__)
log.addHandler(RichHandler())

u = itkdb.core.User(access_code1="fokgoh-miXdyq", access_code2="bysfe6-xebcub")
client = itkdb.Client(user=u)
client.user.authenticate()

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@app.command()
def main(
    serial_number: Annotated[
        str,
        typer.Argument(
            help="Serial number of component to process and recursively update FE chip trim bits for",
        ),
    ],
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run/--execute",
            help="Whether to run in dry run mode or not (actually change things).",
        ),
    ] = True,
):
    """
    Update FE chip trim bit properties for a given component in the ITk Production Database.

    This utility connects to the ITk Production Database, recursively finds all associated FE_CHIP
    components for a given serial number, and updates their `TARGET_IREF_TRIM` and
    `TARGET_IREF_TRIM_VERSION` properties based on the most recent valid `FECHIP_TEST` result
    from the TESTONWAFER stage.



    \bExample:
        python set_iref_trim_pdb.py --execute 20UPG12345

    \b
    Dependencies:
        - itkdb: ITk Production Database client
        - module_qc_database_tools.db.prod: Custom utilities to interact with DB entries

    \b
    Note:
        - Assumes components of type FE_CHIP are the only ones for which IREF_TRIM properties are set.
        - Logs warnings if expected test data is missing or inconsistent.
        - Requires valid authentication/configuration for `itkdb.Client()`.
    """

    if dry_run:
        print("[yellow bold]:exclamation:Dry run mode[/]")

    tree = Tree("Setting properties")

    component, _ = prod.get_component(client, serial_number)

    ctype = component["componentType"]["code"]

    if ctype == "FE_CHIP":
        fe_chips = [prod.get_serial_number(component)]
    else:
        fe_chips = [
            prod.get_serial_number(child)
            for child in prod.get_children(client, component, component_type="FE_CHIP")
        ]

    if not fe_chips:
        log.error("No front-end chips found for %s.", serial_number)
        raise typer.Exit(1)

    for fe_chip_sn in fe_chips:
        test_runs = sorted(
            client.get(
                "listTestRunsByComponent",
                json={
                    "filterMap": {
                        "serialNumber": fe_chip_sn,
                        "testType": ["FECHIP_TEST"],
                        "stage": ["TESTONWAFER"],
                        "state": ["ready"],
                    }
                },
            ),
            key=lambda x: x["date"],
        )
        if not test_runs:
            log.warning(
                "%s is missing the Electrical FE chip tests (FECHIP_TEST).", fe_chip_sn
            )

        if len(test_runs) > 1:
            log.warning(
                "%s has multiple Electrical FE chip tests (FECHIP_TEST). Taking the most recent one.",
                fe_chip_sn,
            )

        test_run_bare = test_runs[-1]
        test_run, tr_sn, tr_stage = prod.get_test_run(client, test_run_bare["id"])
        assert (
            tr_sn == fe_chip_sn
        ), f"The test run we found for {fe_chip_sn} is associated to {tr_sn} for {test_run['id']}. This should not happen."

        results = {result["code"]: result for result in test_run["results"]}
        if "IREF_TRIM" not in results:
            log.warning(
                "%s has a test run %s missing the IREF_TRIM result, skipping.",
                tr_sn,
                test_run["id"],
            )

        iref_trim_bit = results["IREF_TRIM"]["value"]

        subtree = tree.add(fe_chip_sn)
        subtree.add(f"TARGET_IREF_TRIM = {iref_trim_bit + 1}")
        subtree.add("TARGET_IREF_TRIM_VERSION = 1")

        if not dry_run:
            client.post(
                "setComponentProperty",
                json={
                    "component": fe_chip_sn,
                    "code": "TARGET_IREF_TRIM",
                    "value": min(iref_trim_bit + 1, 15),
                },
            )
        if not dry_run:
            client.post(
                "setComponentProperty",
                json={
                    "component": fe_chip_sn,
                    "code": "TARGET_IREF_TRIM_VERSION",
                    "value": "1",
                },
            )

    print(tree)


if __name__ == "__main__":
    app()
