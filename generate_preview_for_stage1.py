import os

from gerber import load_layer
from gerber.render import theme
from gerber.render.cairo_backend import GerberCairoContext

# os.chdir(os.path.dirname(__file__))

INPUT_DIR = "output_stage1/"
OUTPUT_DIR = "output_stage3/"


def setup():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def main():
    setup()

    GERBER_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), INPUT_DIR))

    # Create a new drawing context
    ctx = GerberCairoContext()

    # Create a new PCB instance
    # pcb = PCB.from_directory(GERBER_FOLDER)
    outline = load_layer(INPUT_DIR + 'axiom_beta_mixed_panel.boardoutline.ger')
    outline.layer_class = "outline"
    top_layer = load_layer(INPUT_DIR + 'axiom_beta_mixed_panel.toplayer.ger')
    top_layer.layer_class = "toppaste"
    # top_soldermask_layer = load_layer(INPUT_DIR + 'axiom_beta_mixed_panel.topcream.ger')
    # top_soldermask_layer.layer_class = "toppaste"
    top_silkscreen_layer = load_layer(INPUT_DIR + 'axiom_beta_mixed_panel.topsilkscreen.ger')
    top_silkscreen_layer.layer_class = "topsilk"
    drill = load_layer(INPUT_DIR + 'axiom_beta_mixed_panel.drills.xln')

    # Render PCB top view
    ctx.render_layers({outline, top_layer, top_silkscreen_layer},
                      OUTPUT_DIR + 'pcb_top.png',
                      theme.THEMES['OSH Park'], verbose=True, max_width=4000, max_height=3000)

    # outline = load_layer(INPUT_DIR + '/axiom_beta_mixed_panel.boardoutline.ger')
    # top_layer = load_layer(INPUT_DIR + '/axiom_beta_mixed_panel.toplayer.ger')
    # top_soldermask_layer = PCBLayer(INPUT_DIR + '/axiom_beta_mixed_panel.topmask.ger')
    # drill = load_layer(INPUT_DIR + '/axiom_beta_mixed_panel.drills.xln')

    # top_silkscreen_layer = load_layer(INPUT_DIR + '/axiom_beta_mixed_panel.topsilkscreen.ger')
    # top_silkscreen_layer.layer_class = 'topsilk'

    # ctx = GerberCairoContext(scale=20)

    # bg_settings = RenderSettings(color=theme.COLORS['white'], alpha=0.1)
    # fg_settings = RenderSettings(color=theme.COLORS['blue'])
    # ctx.render_layer(top_layer)
    # ctx.render_layer(top_soldermask_layer)
    # ctx.render_layer(top_silkscreen_layer)
    # ctx.render_layer(outline)  # , settings=fg_settings, bgsettings=bg_settings)
    # ctx.render_layer(drill)

    # ctx.dump(OUTPUT_DIR + '/panel_preview.png')


if __name__ == "__main__":
    # execute only if run as a script
    main()
