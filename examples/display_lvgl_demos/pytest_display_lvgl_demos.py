# SPDX-FileCopyrightText: 2023-2026 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: CC0-1.0

import pytest
from pytest_embedded import Dut


@pytest.mark.runner_esp_box_3
@pytest.mark.runner_esp32_p4_function_ev_board
@pytest.mark.runner_esp32_s3_eye
@pytest.mark.runner_esp32_s3_lcd_ev_board
@pytest.mark.runner_esp32_s3_lcd_ev_board_2
@pytest.mark.runner_m5dial
@pytest.mark.runner_m5stack_core_s3
def test_example_lvgl_demos(dut: Dut) -> None:
    dut.expect_exact('app_main: Display LVGL demo')
    dut.expect_exact('main_task: Returned from app_main()')
