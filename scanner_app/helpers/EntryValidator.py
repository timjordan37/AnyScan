class Validator:

    @staticmethod
    def validateInteger(self, value):
        try:
            integer_result = int(value)
        except ValueError:
            return False
        else:
            return True
