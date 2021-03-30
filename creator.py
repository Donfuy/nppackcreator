from definitions import *
import os
import shutil
from PIL import Image


class Creator:
    def __init__(self):
        self.name = ''
        self.tabs = []
        self.nprofile = ''
        self.attracts = []
        self.banner = ''

    def has_tab(self, checking_tab):
        if self.has_tabs():
            for tab in self.tabs:
                if checking_tab == tab:
                    return True
                if os.path.basename(checking_tab) == os.path.basename(tab):
                    return True
        return False

    def has_tabs(self):
        if len(self.tabs) == 0:
            return False
        else:
            return True

    def add_tabs(self):
        levels_folder = os.path.join(self.name, 'Levels')
        os.mkdir(levels_folder)
        for tab in self.tabs:
            shutil.copy(tab, os.path.join(levels_folder, os.path.basename(tab)))

        # THIS IS NOT NEEDED - WORKS FINE WITHOUT THEM
        # for tab in os.listdir(EMPTY_TABS_FOLDER):
        #     tab_exists = False
        #     for custom_tab in self.tabs:
        #         if os.path.basename(tab) == os.path.basename(custom_tab):
        #             tab_exists = True
        #
        #     if not tab_exists:
        #         empty_tab_path = os.path.join(EMPTY_TABS_FOLDER, tab)
        #         new_tab_path = os.path.join(levels_folder, os.path.basename(tab))
        #         shutil.copy(empty_tab_path, new_tab_path)

    def has_name(self):
        if self.name == '':
            return False
        else:
            return True

    def has_nprofile(self):
        if self.nprofile == '':
            return False
        else:
            return True

    def remove_nprofile(self):
        self.nprofile = ''

    # Generates a nprofiles zip from a supplied nprofile.
    def generate_nprofiles_zip(self):
        os.mkdir('nprofiles')
        shutil.copy(self.nprofile, os.path.join('nprofiles', 'nprofile-old'))
        shutil.copy(self.nprofile, os.path.join('nprofiles', 'nprofile'))
        shutil.make_archive('nprofiles', 'zip', root_dir='nprofiles')
        shutil.rmtree('nprofiles')
        shutil.move('nprofiles.zip', os.path.join(self.name, 'nprofiles.zip'))

    # Generates a clean, gamification enabled nprofiles.zip
    def generate_clean_nprofiles_zip(self):
        shutil.copy(os.path.join('res', 'nprofiles.zip'), os.path.join(self.name, 'nprofiles.zip'))

    def has_attracts(self):
        if len(self.attracts) == 0:
            return False
        else:
            return True

    # Copies supplied attract files to the attract folder
    def add_attracts(self):
        os.mkdir(os.path.join(self.name, 'attract'))
        for attract_file in self.attracts:
            shutil.copy(attract_file, os.path.join('attract', attract_file))

    def remove_attracts(self):
        self.attracts = []

    def has_banner(self):
        if self.banner == '':
            return False
        else:
            return True

    def validate_banner(self):
        try:
            with Image.open(self.banner) as im:
                # Check banner size
                if im.size != BANNER_SIZE:
                    return BANNER_INVALID_SIZE
                return BANNER_VALID
        except OSError:
            # Check if it's an image
            return BANNER_NOT_AN_IMAGE

    def add_banner(self):
        with Image.open(self.banner) as im:
            try:
                im.save(os.path.join(self.name, 'banner.png'))
            except OSError:
                print("Cannot convert", im)

    def remove_banner(self):
        self.banner = ''

    # TODO: Progress indicator cause nprofiles take a while to zip
    def create_pack(self):
        # TODO: surround all file ops with a try catch, to remove the temp folder in case of failure.
        os.mkdir(self.name)
        self.add_tabs()
        # Create nprofiles.zip
        if self.has_nprofile():
            self.generate_nprofiles_zip()
        else:
            self.generate_clean_nprofiles_zip()

        # Create attract folder
        if self.has_attracts():
            self.add_attracts()
        else:
            os.mkdir(os.path.join(self.name, 'attract'))

        # Add banner
        if self.has_banner():
            self.add_banner()

        # TODO: Zip it all up AS A .NPPACK and ask where to save
        shutil.make_archive(self.name, 'zip', root_dir=self.name)
        shutil.copy(self.name + '.zip', self.name + '.nppack')
        shutil.rmtree(self.name)
        os.remove(self.name + '.zip')

