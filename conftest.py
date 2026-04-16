# SPDX-FileCopyrightText: 2024-2026 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0
import os
import uuid
import pytest


build_dir_override = {
    "esp_box_3": "build_esp-box-3",
    "esp32_s3_lcd_ev_board_2":"build_esp32_s3_lcd_ev_board",
    "esp32_s3_devkitc_1_1": "build_esp_bsp_devkit",
    "esp32_s2_devkitc_1": "build_esp_bsp_generic"
}


port_override = {
    "esp_box_3": "/dev/boards/esp-box-3",
    "esp32_s3_lcd_ev_board_2": "esp32_s3_lcd_ev_board-2"
}


def pytest_generate_tests(metafunc):
    test_parameters = []

    for marker in metafunc.definition.iter_markers():
        if marker.name.startswith("runner_"):
            board_name = marker.name.removeprefix("runner_")
            com_port = port_override.get(board_name, f'/dev/boards/{board_name}')
            flash_port = port_override.get(board_name, f'/dev/boards/{board_name}')
            build_dir = build_dir_override.get(board_name, f'build_{board_name}')
            bsp_param = pytest.param(
                com_port,
                flash_port,
                build_dir,
                id=f'{board_name}',
                # Creates a resource group for each board
                marks=pytest.mark.xdist_group(name=f'{board_name}')
            )
            test_parameters.append(bsp_param)

    if 'port' in metafunc.fixturenames and 'flash_port' in metafunc.fixturenames:
        metafunc.parametrize(
            'port, flash_port, build_dir',
            test_parameters
        )


# This fixing using cache when used "-n auto" (parallel)
def pytest_configure(config):
    # If run pytest-xdist (parallel), set unique cache dir
    worker_id = os.getenv("PYTEST_XDIST_WORKER", None)
    if worker_id:
        cache_dir = f"/tmp/pytest-embedded-cache-{uuid.uuid4()}"
        os.environ["PYTEST_EMBEDDED_CACHE_DIR"] = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        print(f"Using embedded cache dir: {cache_dir}")
