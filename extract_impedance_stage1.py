import lxml.etree as ET
import os

INPUT_DIR = "input/EAGLE/"
OUTPUT_DIR = "output_impedance_filtered/"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def extract_impedance(filename):
    tree = ET.parse(INPUT_DIR + filename + "/" + filename + ".brd")
    xml_root = tree.getroot()

    lvds_signals = xml_root.xpath(".//signal[not(@class='1')]")
    for signal in lvds_signals:
        signal.getparent().remove(signal)

        lvds_signals = xml_root.xpath(".//signal")
        for signal in lvds_signals:
            elements = signal.xpath("./*[not(self::wire)]")
            for element in elements:
                signal.remove(element)

        elements = xml_root.xpath("//elements")
        for element in elements:
            element.getparent().remove(element)

        file = open(OUTPUT_DIR + filename + "_impedance.brd", "w")
        file.write(ET.tostring(tree.getroot()).decode("utf-8"))


extract_impedance("axiom_beta_sensor_cmv12000_tht_v0.16_r1.6c")
extract_impedance("axiom_beta_interface_dummy_v0.13_r1.4")
extract_impedance("axiom_beta_main_board_v0.37_r1.2")
extract_impedance("axiom_beta_power_board_v0.37_r1.3")
extract_impedance("test_strip_v0.1_r1.2")
