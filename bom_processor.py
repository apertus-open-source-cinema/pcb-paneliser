import csv
import os

BOM_FILE = "input/BOM/BOM.tsv"
EAGLE_DATA_DIR = "input/EAGLE/"
OUTPUT_DIR = "output_bom/"
csv_data = []

top_components = {}
bottom_components = {}

field_names = []


def determine_side(components, pcb_name):
    top = 0
    bottom = 0

    for component in components:
        if component in top_components[pcb_name]:
            top = top + 1
        if component in bottom_components[pcb_name]:
            bottom = bottom + 1

    # top = set(components) <= set(top_components[pcb_name])
    # bottom = set(components) <= set(bottom_components[pcb_name])

    side = "N/A"
    if top > 0 and bottom > 0:
        side = "TOP/BOT"
    else:
        if top > 0:
            side = "TOP"
        if bottom > 0:
            side = "BOT"
    return side


def rename_pcb_components(components, pcb_name):
    components_pcb = []
    for component in components:
        components_pcb.append(format(component + "_" + pcb_name))
    return components_pcb


def load_bom_components():
    with open(BOM_FILE) as bom_file:
        for i in range(4):
            next(bom_file)
        reader = csv.DictReader(bom_file, delimiter='\t')
        global field_names
        field_names = reader.fieldnames
        for row in reader:
            if row["ID"] == '':
                continue

            pcb_name = row["PCB"][:2]

            components = row["Schematic Reference (Silkscreen)"].split(',')
            components = [x.strip(' ') for x in components]

            components_pcb = rename_pcb_components(components, pcb_name)
            row["Combined Sch. Reference (*.asc)"] = ",".join(components_pcb)

            side = determine_side(components, pcb_name)
            row["Side"] = side
            csv_data.append(row)


def get_components_list(file):
    components = []

    for line in file:
        name, x, y, rotation, *temp = line.split()
        components.append(name)

    return components


def get_components(pcb_name, suffix):
    file = open(EAGLE_DATA_DIR + pcb_name + "/" + pcb_name + ".mnt", "r")
    components = get_components_list(file)
    top_components[suffix] = components

    file = open(EAGLE_DATA_DIR + pcb_name + "/" + pcb_name + ".mnb", "r")
    components = get_components_list(file)
    bottom_components[suffix] = components


def write_bom():
    with open(OUTPUT_DIR + 'test_bom.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, field_names, delimiter=";")
        writer.writeheader()
        writer.writerows(csv_data)


def setup():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def main():
    setup()

    get_components("axiom_beta_main_board_v0.37_r1.1", "MB")
    get_components("axiom_beta_power_board_v0.37_r1.2", "PB")
    get_components("axiom_beta_interface_dummy_v0.13_r1.3", "IB")
    get_components("axiom_beta_sensor_cmv12000_tht_v0.16_r1.5c", "SB")

    load_bom_components()

    write_bom()


if __name__ == "__main__":
    # execute only if run as a script
    main()
