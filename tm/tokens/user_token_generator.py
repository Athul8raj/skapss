import random as r

class User_token_generator:

    def make_token(self):
        """
        Return a token that can be used once to do a token check
        for the given user.
        """
        return self.make_uuid()

    def make_uuid(self):
        random_string = ''
        random_str_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        uuid_format = [8, 4, 4, 4, 12]
        for n in uuid_format:
            for i in range(0,n):
                random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])
            if n != 12:
                random_string += '-'
        
        return random_string
    
