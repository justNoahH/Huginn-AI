import cv2
import face_recognition
import numpy as np
import os
from customtkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from deepface import DeepFace

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Huginn AI")
        self.root.geometry("1080x720")
        self.root.resizable(False, False)

        self.credit = CTkLabel(master=root, text="Created by HERBELIN--ALVES Noah")
        self.credit.pack(anchor="nw")

        self.gui_start_stop = CTkFrame(master=root)
        self.gui_start_stop.place(x=50, y=50)

        self.gui_db = CTkFrame(master=root)
        self.gui_db.place(x=300, y=50)

        self.gui_more = CTkFrame(master=root)
        self.gui_more.place(x=600, y=50)

        self.gui_settings = CTkFrame(master=root)
        self.gui_settings.place(x=850, y=50)

        self.web_results = CTkFrame(master=root)
        self.web_results.place(x=35, y=360)

        self.video_label = CTkLabel(master=root, text="")
        self.video_label.pack(expand=True, anchor="s")

        self.label_start = CTkLabel(master=self.gui_start_stop, text="Menu démarrage", font=("Source Code Pro", 14))
        self.label_db = CTkLabel(master=self.gui_db, text="Choisissez les bases de données")
        self.label_more = CTkLabel(master=self.gui_more, text="Plus d'options")
        self.label_settings = CTkLabel(master=self.gui_settings, text="Paramètres")
        self.label_web_results = CTkLabel(master=self.web_results, text="Résultats Web :")
        self.label_start.pack(expand=True, pady=10)
        self.label_db.pack(expand=True, pady=10, padx=30)
        self.label_more.pack(expand=True, pady=10)
        self.label_settings.pack(expand=True, pady=10)
        self.label_web_results.pack(expand=True, padx=10, pady=10)

        self.start_button = CTkButton(master=self.gui_start_stop, text="Démarrer", command=self.start_recognition, corner_radius=32,
                                      border_width=2)
        self.start_button.pack(expand=True, padx=30, anchor="n")

        self.stop_button = CTkButton(master=self.gui_start_stop, text="Arrêter", command=self.stop_recognition, corner_radius=32,
                                     border_width=2)
        self.stop_button.pack(expand=True, pady=10, padx=30, anchor="n")

        self.web = CTkButton(master=self.gui_more, text="Recherche Web", command=self.web, corner_radius=32,
                                     border_width=2)
        self.web.pack(expand=True, padx=30, anchor="n")

        #self.db_choice = CTkComboBox(master=self.gui, values=["Polytech", "Célébrités", "Web"])
        #self.db_choice.pack(pady=10, anchor="s")

        self.celeb = CTkCheckBox(master=self.gui_db, text="Célébrités")
        self.celeb.pack(expand=True, pady=5, padx=5, anchor="s")
        self.polytech = CTkCheckBox(master=self.gui_db, text="Polytech")
        self.polytech.pack(expand=True, pady=9, padx=5, anchor="s")

        self.predictions_gui = CTkFrame(master=root, width=160, height=212)
        self.predictions_gui.place(x=930, y=360)

        self.predictions_button = CTkButton(master=self.gui_more, text="Prédictions", command=self.predictions,
                                      corner_radius=32, border_width=2)
        self.predictions_button.pack(expand=True, pady=10, padx=30, anchor="center")

        self.predictions_text = CTkLabel(master=self.predictions_gui, text="Prédictions :")
        self.predictions_text.pack(expand=True, anchor="n", padx=10, pady=10)

        self.choose_device = StringVar(value="Périphérique")
        self.devices = self.list_devices()

        self.device = CTkOptionMenu(master=self.gui_settings, variable=self.choose_device, values=self.devices)
        self.device.pack(expand=True, padx=30)

        self.choose_theme = StringVar(value="Choisir un thème")
        self.theme = CTkOptionMenu(master=self.gui_settings, variable=self.choose_theme, values=["Sombre", "Clair", "Système"], command=self.select_theme)
        self.theme.pack(expand=True, padx=30, pady=10)


        self.video_capture = None
        self.running = False
        self.current_frame = None
        self.face_locations = []

        self.known_face_encodings, self.known_face_names = self.load_face_encodings(r"répertoire")

    def load_face_encodings(self, directory):
        if self.celeb.get()==1 and self.polytech.get()==1:
            directory = r"répertoire"
        elif self.celeb.get()==1:
            directory = r"répertoire"
        elif self.polytech.get()==1:
            directory = r"répertoire"

        encodings = []
        names = []
        for filename in os.listdir(directory):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(directory, filename)
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)[0]
                encodings.append(encoding)
                names.append(filename.split("_")[0])
                print(f"Chargement de l'image {filename}: shape={image.shape}, dtype={image.dtype}")
            else:
                print(f"Aucun visage trouvé dans {filename}")
        return encodings, names

    def start_recognition(self):
        if not self.running:
            try:
                selected_device = self.choose_device.get()

                if selected_device == "Périphérique":
                    raise ValueError("Veuillez sélectionner un périphérique vidéo.")

                self.running = True
                self.process_video()

            except Exception:
                messagebox.showerror("Erreur", "Veuillez sélectionner un périphérique vidéo.")



    def stop_recognition(self):
        if self.running:
            self.running = False
            self.video_capture.release()
            self.video_label.configure(image='')

    def process_video(self):
        if self.running:
            self.video_capture = cv2.VideoCapture(int(self.choose_device.get().split()[-1]) - 1)
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.resize(frame, (1440, 960))

                # Convertir BGR à RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Détecter les emplacements des visages et les encodages
                self.face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, self.face_locations)

                for (top, right, bottom, left), face_encoding in zip(self.face_locations, face_encodings):
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Inconnu"

                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]

                    if name == "Inconnu":
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 1)
                    else:
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 1)

                # Convertir l'image BGR pour l'affichage
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                photo = ImageTk.PhotoImage(image=image)
                self.video_label.configure(image=photo)
                self.video_label.photo = photo

                self.current_frame = frame


            self.root.after(10, self.process_video)

    def web(self):
        if self.current_frame is not None and self.face_locations:
            for i, (top, right, bottom, left) in enumerate(self.face_locations):
                face_image = self.current_frame[top:bottom, left:right]
                filename = f"captured_face_{i}.jpg"
                cv2.imwrite(filename, face_image)
                print(f"Face capturée et enregistrée comme {filename}")

    def predictions(self):
        if self.current_frame is not None and self.face_locations and self.running:

            face_image = self.current_frame
            filename = f"captured_face.jpg"
            cv2.imwrite(filename, face_image)
            print(f"Face capturée et enregistrée comme {filename}")

            results = DeepFace.analyze(face_image, actions=("emotion", "age", "gender", "race"))
            data = {
                "Genre": [],
                "Age": [],
                "Ethnie": [],
                "Emotion": []
            }
            data["Genre"].append(results[0]["dominant_gender"])
            data["Age"].append(results[0]["age"])
            data["Ethnie"].append(results[0]["dominant_race"])
            data["Emotion"].append(results[0]["dominant_emotion"])

            self.predictions_text.configure(text=f"Prédictions :\n\nGenre : {data["Genre"][0]}"
                                                 f"\nAge : {data["Age"][0]}"
                                                 f"\nEthnie : {data["Ethnie"][0]}"
                                                 f"\nEmotion : {data["Emotion"][0]}")
            self.predictions_text.update_idletasks()

    def select_theme(self, choice):
        if choice == "Sombre":
            set_appearance_mode("dark")
            set_default_color_theme("dark-blue")
        elif choice == "Clair":
            set_appearance_mode("light")
            set_default_color_theme("green")
        else:
            set_appearance_mode("system")

    def list_devices(self):
        index = 0
        devices = []
        indexes = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                devices.append(f"Caméra {index+1}")
                indexes.append(index)
            cap.release()
            index += 1
        return devices


if __name__ == "__main__":
    root = CTk()
    app = App(root)
    set_appearance_mode("dark")
    set_default_color_theme("dark-blue")
    root.mainloop()

