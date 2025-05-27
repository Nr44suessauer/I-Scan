import cv2
import numpy as np


class USBCam:
    def __init__(self, device_index=0):
        self.cap = cv2.VideoCapture(device_index)

    def verbinden(self):
        return self.cap.isOpened()

    def jpeg_frame_lesen(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        return None

    @property
    def verbindung(self):
        class Dummy:
            def close(inner_self):
                self.cap.release()

        return Dummy()


def stream_starten(self):
    """Kamerastream starten und anzeigen mit Foto-Option"""
    if not self.verbinden():
        return

    cv2.namedWindow("Kamera-Stream", cv2.WINDOW_NORMAL)
    bild_zaehler = 0

    try:
        print("Kamera-Stream gestartet. Befehle:")
        print("'s': Foto aufnehmen")
        print("'q': Stream beenden")

        while True:
            frame = self.jpeg_frame_lesen()

            if frame is not None:
                # Hilfsinformationen ins Bild einblenden
                info_text = "s: Foto aufnehmen | q: Beenden"
                cv2.putText(
                    frame,
                    info_text,
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )

                cv2.imshow("Kamera-Stream", frame)

            # Tastatureingaben prüfen
            key = cv2.waitKey(1) & 0xFF
            if key == ord("s"):  # Taste 's' zum Speichern des Fotos
                if frame is not None:
                    dateiname = f"kamera_bild_{bild_zaehler}.jpg"
                    cv2.imwrite(dateiname, frame)
                    print(f"Foto gespeichert als: {dateiname}")
                    bild_zaehler += 1
            elif key == ord("q"):  # Taste 'q' zum Beenden
                break

    finally:
        self.verbindung.close()
        cv2.destroyAllWindows()
        print("Stream beendet")


if __name__ == "__main__":
    cam = USBCam(0)  # 0 ist meist die erste USB-Kamera
    stream_starten(cam)
