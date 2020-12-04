from pathlib import Path


def create_folder(folder_name: str):
    folder_path = Path(folder_name)
    if not folder_path.exists():
        folder_path.mkdir()
    return folder_path


def file_name_gen(file_name: str, ext_flag: str, output_folder: str = "output") -> str:
    """
    Args:
        file_name: Name of generated file name.
        ext_flag: Ext Flag determines what file type
            you want to work with. Supported files types
            ['JSON', 'CSV'].
        output_folder: Name of the output folder.
            Defaults to "output".
    Returns:
        A file_name as a string.
    """

    counter = 1
    ext_map = {
        "JSON": ".json",
        "CSV": ".csv",
    }

    ext = ext_map.get(ext_flag.upper())
    if ext is None:
        raise NotImplementedError()

    output_folder = create_folder(output_folder)

    if Path(output_folder / f"{file_name}{ext}").exists():
        while True:
            if not Path(output_folder / f"{file_name}{counter}{ext}").exists():
                return output_folder / f"{file_name}{counter}{ext}"
            counter += 1
    else:
        return output_folder / f"{file_name}{ext}"
