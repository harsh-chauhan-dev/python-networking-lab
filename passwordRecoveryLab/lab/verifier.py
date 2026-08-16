class LocalVerifier:

    def __init__(self,secret):
        self.secret = secret

    def verify(self,candidate):
      """
      Verify a candidate against our local test secret.
      """

      return candidate ==self.secret

    