from typing import Iterable, List

from cimsparql.constants import union_split
from cimsparql.enums import Power
from cimsparql.query_support import acdc_terminal, combine_statements, group_query


def disconnected(cim_version: int) -> str:
    disconnector = [
        "?mrid ?p cim:Disconnector",
        "?mrid cim:Switch.open ?status",
        "filter (?status = True)",
    ]

    terminal = [
        "?mrid ?p cim:Terminal",
        f"?mrid cim:{acdc_terminal(cim_version)}.connected ?connected",
        "filter (?connected = False)",
    ]

    where_list = group_query(
        [combine_statements(*comp, group=True, split=" .\n") for comp in [disconnector, terminal]],
        split=union_split,
    )
    return combine_statements("select ?mrid", where_list)


def synchronous_machines() -> str:
    select = "select ?mrid ?p ?q ?controlEnabled"
    where_list = [
        "?mrid rdf:type cim:SynchronousMachine",
        "?mrid cim:RotatingMachine.p ?p",
        "?mrid cim:RotatingMachine.q ?q",
        "?mrid cim:RegulatingCondEq.controlEnabled ?controlEnabled",
    ]
    return combine_statements(select, group_query(where_list))


def _load(rdf_type: str) -> str:
    return " .\n".join(
        [f"?mrid rdf:type {rdf_type}"] + [f"?mrid cim:EnergyConsumer.{s} ?{s}" for s in Power]
    )


def load(rdf_types: List[str]) -> str:
    query = "\nselect ?mrid ?p ?q\nwhere {{\n"
    query += union_split.join([_load(rdf_type) for rdf_type in rdf_types])
    query += "}}\n"
    return query


def _generating_unit(rdf_type: str) -> str:
    return " .\n".join(
        [f"?mrid rdf:type {rdf_type}", "?mrid cim:GeneratingUnit.normalPF ?normalPF"]
    )


def generating_unit(rdf_types: Iterable[str]) -> str:
    query = "select ?mrid ?normalPF \n where {{\n"
    query += union_split.join([_generating_unit(rdf_type) for rdf_type in rdf_types])
    query += "}}\n"
    return query
