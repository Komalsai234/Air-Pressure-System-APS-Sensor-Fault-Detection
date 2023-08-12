import sys


def error_message_detail(error, error_message):

    _, _, exec_itr = error_message.exc_info()
    file_name = exec_itr.tb_frame.f_code.co_filename

    return f"The Error {0} occured in python file {1} at line number {2}".format(str(error), file_name, exec_itr.tb_lineno)


class exception(Exception):

    def __init__(self, error_meassage, error_detail):
        super.__init__(Exception)

        self.error = error_message_detail(error_meassage, error_detail)

    def __str__(self):
        return str(self.error)
