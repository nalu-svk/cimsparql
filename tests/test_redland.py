import pytest

import numpy as np

from cimsparql import ssh_queries as queries
from cimsparql import redland

from conftest import need_cim_ssh


@pytest.fixture(scope="module")
def sshmodel(root_dir, identifier):
    return redland.Model(root_dir / "data" / f"{identifier}.xml", base_uri="http://example.org")


@need_cim_ssh
def skip_test_model_ssh_components(sshmodel, cim16):
    query = str(cim16) + "\n\nselect distinct ?o \n where { ?s rdf:type ?o . }"

    # print(sshmodel.get_table(query))
    for r in sshmodel.get_table(query)["o"]:
        print(r)


@need_cim_ssh
def test_model_ssh_synchronous_machine(sshmodel, cim16):
    synchronous_machines = queries.ssh_synchronous_machines(sshmodel, str(cim16))
    assert list(synchronous_machines.columns) == ["mrid", "p", "q", "controlEnabled"]
    assert len(synchronous_machines) == 2296


@need_cim_ssh
def test_ssh_disconnected(sshmodel, cim16):
    disconnected = queries.ssh_disconnected(sshmodel, str(cim16))
    assert list(disconnected.columns) == ["mrid"]
    assert len(disconnected) == 7878


@need_cim_ssh
def test_ssh_conformed_load(sshmodel, cim16):
    load = queries.ssh_load(sshmodel, str(cim16))
    assert list(load.columns) == ["mrid", "p", "q"]
    assert len(load) == 1856


@need_cim_ssh
def test_ssh_nonconformed_load(sshmodel, cim16):
    load = queries.ssh_load(sshmodel, str(cim16), conform=False)
    assert list(load.columns) == ["mrid", "p", "q"]
    assert len(load) == 194


@need_cim_ssh
def test_ssh_combined_load(sshmodel, cim16):
    load = queries.ssh_combined_load(sshmodel, str(cim16))
    assert list(load.columns) == ["mrid", "p", "q"]
    assert len(load) == 1856 + 194


@need_cim_ssh
def test_ssh_hydro_generating_unit(sshmodel, cim16):
    hydro = queries.ssh_hydro_generating_unit(sshmodel, str(cim16))
    assert np.all(hydro == 0.0)
    assert len(hydro) == 2177


@need_cim_ssh
def test_ssh_thermal_generating_unit(sshmodel, cim16):
    thermal = queries.ssh_thermal_generating_unit(sshmodel, str(cim16))
    assert np.all(thermal == 0.0)
    assert len(thermal) == 40


@need_cim_ssh
def test_ssh_wind_generating_unit(sshmodel, cim16):
    wind = queries.ssh_wind_generating_unit(sshmodel, str(cim16))
    assert np.all(wind == 0.0)
    assert len(wind) == 71


@need_cim_ssh
def test_ssh_generating_unit_union(sshmodel, cim16):
    gen = queries.ssh_generating_unit_union(
        sshmodel,
        str(cim16),
        ["cim:HydroGeneratingUnit", "cim:ThermalGeneratingUnit", "cim:WindGeneratingUnit"],
    )
    assert np.all(gen == 0.0)
    assert len(gen) == 40 + 2177 + 71
