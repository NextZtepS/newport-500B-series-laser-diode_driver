from ..newport_laser_driver import NewportLaserDriver

model_535B = NewportLaserDriver(idVendor=0x104d, idProduct=0x1001)
model_535B.clear_buffer()

def test_identity():
    assert model_535B._dev.manufacturer == "Newport"
    assert model_535B._dev.product == "Model 300/500"
    assert model_535B.get_identification().__contains__("NEWPORT")


#? Getting error message leads to timeout error
# def test_no_error():
#     assert model_535B.get_error() == ("0", "No error")


def test_key_status_on():
    model_535B.get_key_switch_status() == 1


def test_set_and_get_current_set_point():
    model_535B.set_current_set_point(5.0)
    assert round(model_535B.get_current_set_point(), 1) == 5.0


def test_set_and_get_photodiode_current_set_point():
    model_535B.set_photodiode_current_set_point(5.0)
    assert round(model_535B.get_photodiode_current_set_point(), 1) == 5.0


def test_set_and_get_current_limit():
    model_535B.set_current_limit(50.0)
    assert round(model_535B.get_current_limit(), 0) == 50


def test_constanst_current_mode():
    model_535B.enter_constant_current_mode()
    assert model_535B.get_laser_mode() == "Ilbw" or model_535B.get_laser_mode() == "Ihbw"


def test_constanst_photodiode_current_mode():
    model_535B.enter_constant_photodiode_current_mode()
    assert model_535B.get_laser_mode() == "Mdi"


def test_enable_laser_output():
    model_535B.enable_laser_output()
    assert model_535B.get_laser_output_enable() == 1


def test_disable_laser_output():
    model_535B.disable_laser_output()
    assert model_535B.get_laser_output_enable() == 0


def test_laser_range():
    model_535B.set_laser_range_low()
    assert model_535B.get_laser_range() == 0

    model_535B.set_laser_range_high()
    assert model_535B.get_laser_range() == 1
