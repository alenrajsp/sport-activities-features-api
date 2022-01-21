import uuid

from starlette.responses import FileResponse


def save_temp_plot_image(plot):
    unique = str(uuid.uuid4())
    name = f'temp/{unique}.png'
    plot.savefig(f'temp/{unique}.png')
    response = FileResponse(name)
    return name, response
