requests = []

class User():
    def __init__(self, username, password, reenter_password):
        self.username = username
        self.password = password
        self.reenter_password = reenter_password

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_reenter_password(self):
        return self.reenter_password

class Request():
    def __init__(self, id, device_type, fault_description, device_status):
        self.id = id
        self.device_type = device_type
        self.fault_description = fault_description
        self.device_status = device_status

    def get_device_type(self):
        return self.device_type

    def get_fault_description(self):
        return self.fault_description

    def get_id(self):
        return self.id

    def get_device_status(self):
        return self.device_status