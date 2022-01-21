import os
from sport_activities_features import GPXFile, TCXFile


def read_file(file, filename):
    if file.filename.endswith('.gpx'):
        gpx_file = GPXFile()
        bytes = file.file.read()
        with open(f"temp/{filename}.gpx", 'wb+') as file_obj:
            file_obj.write(bytes)
        file = gpx_file.read_one_file(f"temp/{filename}.gpx")
        os.remove(f"temp/{filename}.gpx")
    elif file.filename.endswith('.tcx'):
        tcx_file = TCXFile()
        file = tcx_file.read_one_file(file.file)
    else:
        file = None
    return file