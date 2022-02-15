import os

import PyPDF2
from PIL import Image


class ImagesExtractor:

    _save_to: str
    _page_counter: int
    _image_counter: int
    _file_name_only: str

    _COLOR_SPACES = {
        '/DeviceRGB': "RGB",
        '/DeviceCMYK': "CMYK",
        '/DeviceGray': "L"
    }

    _FILTER_TO_EXTENSION = {
        '/DCTDecode': '.jpg',
        '/JPXDecode': '.jp2'
    }

    def extract_dir(self, folder: str, save_to: str):
        """
        Extracts images from all PDF-files in a folder
        """
        assert os.path.isdir(folder), f"Not a folder: {folder}"

        files = os.listdir(folder)
        files = [os.path.join(folder, f) for f in files]
        files.sort()
        files = [f for f in files if f.lower().endswith('.pdf')]
        for f in files:
            print(f"File: {f}")
            self.extract_file(f, save_to)

    def extract_file(self, file: str, save_to: str):
        """
        Extracts images from single PDF-file
        """
        self._page_counter = 0
        self._image_counter = 0
        self._file_name_only = os.path.basename(file)

        assert os.path.isdir(save_to), f"Not a folder: {save_to}"
        self._save_to = save_to

        with open(file, "rb") as f:
            input1 = PyPDF2.PdfFileReader(f)
            for page in input1.pages:
                self._page_counter += 1
                try:
                    self._work_obj(page['/Resources']['/XObject'])
                except KeyError:
                    pass

    def _parse_image(self, obj):

        # All objects we need has dict as one of parent classes.
        if not isinstance(obj, dict):
            return

        try:
            subtype = obj['/Subtype']
        except (KeyError, TypeError) as e:
            return

        if subtype != '/Image':
            return

        size = (obj['/Width'], obj['/Height'])
        data = obj.getData()
        cs = obj['/ColorSpace']
        try:
            mode = self._COLOR_SPACES[cs]
        except KeyError as e:
            raise ValueError(f'Unknown color space: {repr(cs)}')

        name_only = f"{self._file_name_only}_p{self._page_counter:03}_i{self._image_counter:05}-{mode}"
        full_name_wo_ext = os.path.join(self._save_to, name_only)

        filter_ = obj['/Filter']
        if filter_ == '/FlateDecode':
            img = Image.frombytes(mode, size, data)
            full_name = full_name_wo_ext + ".jpg"
            img.save(full_name, quality=95)
        elif filter_ in self._FILTER_TO_EXTENSION:
            ext = self._FILTER_TO_EXTENSION[filter_]
            full_name = full_name_wo_ext + ext
            with open(full_name, "wb") as save_file:
                save_file.write(data)
                save_file.close()
        else:
            raise ValueError(f"Unknown '/Filter' value: {repr(filter_)}")

        self._image_counter += 1
        print(f" - Saved {full_name}")


    def _work_obj(self, obj):
        self._parse_image(obj)
        if isinstance(obj, dict):
            for v in obj.keys():
                self._work_obj(obj[v])
