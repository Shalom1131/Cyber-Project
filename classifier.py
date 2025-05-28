import numpy as np
import librosa


class Classifier:
    def __init__(self):
        from tensorflow.keras.models import load_model
        # טען את המודלים שלך (שינוי לפי הנתיבים שלך)
        self.face_model = load_model("models/face_model.h5")
        self.voice_model = load_model("models/voice_model.h5")

    def predict_face(self, image_path):
        from tensorflow.keras.utils import load_img, img_to_array
        img = load_img(image_path, target_size=(224, 224))
        img = img_to_array(img) / 255.0
        img = np.expand_dims(img, axis=0)
        preds = self.face_model.predict(img)
        return preds

    def prepare_voice(self, audio_path):
        expected_mfcc_shape = (43, 232)

        # טען את האודיו בתדר של 16kHz
        y, sr = librosa.load(audio_path, sr=16000)

        # נירמול בסיסי
        y = librosa.util.normalize(y)

        # חישוב MFCC
        hop_length = 512
        required_length = (expected_mfcc_shape[1] - 1) * hop_length

        if len(y) < required_length:
            y = np.pad(y, (0, required_length - len(y)), mode='constant')

        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=expected_mfcc_shape[0], hop_length=hop_length)

        # גזירה או ריפוד לצורה הרצויה
        if mfccs.shape[1] > expected_mfcc_shape[1]:
            mfccs = mfccs[:, :expected_mfcc_shape[1]]
        elif mfccs.shape[1] < expected_mfcc_shape[1]:
            pad_width = expected_mfcc_shape[1] - mfccs.shape[1]
            mfccs = np.pad(mfccs, ((0, 0), (0, pad_width)), mode='constant')

        mfccs = mfccs[..., np.newaxis]  # Channel dimension
        mfccs = np.expand_dims(mfccs, axis=0)  # Batch dimension
        return mfccs

    def predict_voice(self, audio_path):
        mfccs = self.prepare_voice(audio_path)
        preds = self.voice_model.predict(mfccs)
        return preds
