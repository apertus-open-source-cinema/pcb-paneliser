import lxml.etree as ET

INPUT_DIR = "input/EAGLE/axiom_beta_sensor_cmv12000_tht_v0.16_r1.6c/"
file = 'axiom_beta_sensor_cmv12000_tht_v0.16_r1.6c.brd'
tree = ET.parse(INPUT_DIR + file)
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

file = open("output.xml.brd", "w")
file.write(ET.tostring(tree.getroot()).decode("utf-8"))
