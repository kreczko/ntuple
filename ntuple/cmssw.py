'''
    Converter for the CMS SoftWare (CMSSW).
    It requires a fully set up CMSSW area
'''


class CMSSWConverter():

    def __init__(self):
        # check if CMSSW_BASE is set
        import os
        is_cmssw_set_up = 'CMSSW_base' in os.environ
        if not is_cmssw_set_up:
            import sys
            sys.exit('CMSSW does not seem to be set up, aborting...')

    def convert_file_path(self, file_path):
        # call edmFileUtil -d file_path
        pass
