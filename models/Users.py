from dataclasses import dataclass

# Define the model class
# FirstName = firstname,
# LastName=lastname,
# Email=email,
# Password=password,
# MobileNumber=mobileNumber,
# Designation=designation,
# Token=generate_jwt(email,password),
@dataclass
class User:
    firstname: str
    lastname: str
    email: str
    password: str
    mobilenumber: str
    designation: str
    token: 'Token'

    def to_dict(self):
        return {
            'FirstName': self.firstname,
            'LastName': self.lastname,
            'Email': self.email,
            'Password': self.password,
            'MobileNumber': self.mobilenumber,
            'Designation': self.designation,
            'Token': {
                'AccessToken': self.token.access_token,
                'ExpirationTimestamp': self.token.expiration_timestamp
            }
        }
@dataclass
class Token:
    access_token: str
    expiration_timestamp: int