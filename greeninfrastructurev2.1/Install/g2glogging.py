import os
import datetime

class Logging(object):
    def __init__(self,projectPath=""):
        if projectPath!="":
            self._current_directory = projectPath
        else:
            self._current_directory = os.path.dirname(os.path.realpath(__file__))
        self._log_file_name = "g2g_log.txt"
        self._overwrite = False

    def write_output(self, value):
        dtstr = unicode(datetime.datetime.now()) + "\n\n"
        if self._overwrite == False:
            outfile = self._current_directory + "\\" + self._log_file_name
            with open(outfile,"a") as writeFile:
                writeFile.write(dtstr)
                writeFile.write(value)
                writeFile.write("\n\n+++++++++++++++++++++++\n\n")
    def set_overwrite(self,overwrite):
        """Should be boolean"""
        self._overwrite = overwrite



# test = Logging()
# test.write_output("This is the test string")