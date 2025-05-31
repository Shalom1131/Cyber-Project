class AuthResult:
    def __init__(self, face_name, voice_name):
        self.face_name = face_name
        self.voice_name = voice_name

    @property
    def success(self):
        return self.face_name == self.voice_name and self.face_name not in ["Unknown", "Background noise"]

    def __str__(self):
        if self.success:
            return f"Authentication successful: Face={self.face_name}, Voice={self.voice_name}"
        else:
            return f"Authentication failed: Face={self.face_name}, Voice={self.voice_name}"
