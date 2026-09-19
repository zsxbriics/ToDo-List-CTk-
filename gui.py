import json
import customtkinter as ctk
import os
import sys

basis = os.getenv("LOCALAPPDATA")
ordner = os.path.join(basis, "ToDo")
os.makedirs(ordner, exist_ok=True)
datei = os.path.join(ordner, "todos.json")

def ressource_path(dateiname):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, dateiname)
    return dateiname

def speichere_todos():
    with open(datei, "w") as f:
        json.dump(todos, f)

def lade_todos():
    try:
        with open(datei, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def aktualisiere_anzeige():
    zeige_stats()
    auswahl = kategories_filter_var.get()
    for widget in liste_frame_aktiv.winfo_children():
        widget.destroy()
    for widget in liste_frame_erledigt.winfo_children():
        widget.destroy()

    for index, todo in enumerate(todos):
        kat = todo.get("Kategorie", "Sonstiges")
        if auswahl != "Ohne Filter" and kat != auswahl:
            continue
        if todo["Erledigt"]:
            ziel_frame = liste_frame_erledigt
        else:
            ziel_frame = liste_frame_aktiv
        zeile = ctk.CTkFrame(ziel_frame)
        zeile.pack(fill="x", pady=4, padx=4)

        inhalt_frame = ctk.CTkFrame(zeile, fg_color="transparent")
        inhalt_frame.pack(side="left", fill="x", expand=True, padx=10, pady=8)

        var = ctk.BooleanVar(value=todo["Erledigt"])
        if todo["Prioritaet"] == "Hoch":
            prio_symbol = "🔴"
        elif todo["Prioritaet"] == "Mittel":
            prio_symbol = "🟡"
        else:
            prio_symbol = "🟢"

        checkbox = ctk.CTkCheckBox(
            inhalt_frame,
            text=f"{prio_symbol} {todo['Aufgabe']} [ {kat} ]",
            variable = var,
            command=lambda i=index: markieren(i)
        )

        checkbox.pack(padx=10, pady=8, anchor="w")

        if todo["Beschreibung"]:
            description = ctk.CTkLabel(
                inhalt_frame,
                text=todo["Beschreibung"],
                font=ctk.CTkFont(size=11),
                text_color="grey",
                anchor="w",
                justify="left",
                wraplength=250
            )
            description.pack(padx=10, pady=8, anchor="w")


        loeschen_button = ctk.CTkButton(
            zeile,
            text="Löschen",
            width=80,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=lambda i=index: loeschen(i)
        )
        loeschen_button.pack(side="right", padx=10, pady=8)

        bearbeiten_button = ctk.CTkButton(
            zeile,
            text="Bearbeiten",
            width=80,
            fg_color="#20A100",
            hover_color="#0b8300",
            command=lambda i=index: beschreibung_bearbeiten(i)
        )
        bearbeiten_button.pack(side="right", padx=10, pady=8)


def zeige_stats():
    erledigt_anzahl = 0
    for todo in todos:
        if todo["Erledigt"]:
            erledigt_anzahl = erledigt_anzahl + 1

    gesamt = len(todos)
    statistic_label.configure(text=f"{erledigt_anzahl} von {gesamt} Todos erledigt.")

def hinzufuegen():
    aufgabe = eingabe.get()
    description = eingabe1.get()
    kat = kategorie_menu.get()
    if aufgabe != "":
        todos.append({"Aufgabe": aufgabe, "Beschreibung": description, "Prioritaet": "Mittel", "Kategorie": kat, "Erledigt": False})
        speichere_todos()
        aktualisiere_anzeige()
        eingabe.delete(0, "end")
        eingabe1.delete(0, "end")
    

def beschreibung_bearbeiten(index):
    popup = ctk.CTkToplevel(fenster)
    popup.title("Todo bearbeiten")
    popup.geometry("400x300")
    popup.iconbitmap(ressource_path("logo.ico"))

    label_prio = ctk.CTkLabel(popup, text="Priorität & Kategorie")
    label_prio.pack(pady=5)


    prioritaet_var = ctk.StringVar(value=todos[index]["Prioritaet"])
    prioritaet_wert = ctk.CTkOptionMenu(
        popup, 
        values=["Hoch", "Mittel", "Niedrig"], 
        variable=prioritaet_var
        )
    prioritaet_wert.pack(pady=2.5)

    change_kategorie_var = ctk.StringVar(value=todos[index].get("Kategorie", "Sonstiges"))
    change_kategorie_menu = ctk.CTkOptionMenu(
        popup,
        values=["Python", "C#", "C++", "Java", "JavaScript", "Sonstiges"],
        variable=change_kategorie_var
        )
    change_kategorie_menu.pack(pady=2.5)

    popup.lift()
    popup.attributes("-topmost", True)
    popup.focus_force()

    label_beschreibung = ctk.CTkLabel(popup, text="Beschreibung:")
    label_beschreibung.pack(pady=(20, 5))


    eingabe_popup = ctk.CTkEntry(popup, width=300)
    eingabe_popup.pack(pady=5)
    eingabe_popup.insert(0, todos[index]["Beschreibung"])

    def speichern():
        todos[index]["Beschreibung"] = eingabe_popup.get()
        todos[index]["Prioritaet"] = prioritaet_var.get()
        todos[index]["Kategorie"] = change_kategorie_var.get()
        speichere_todos()
        aktualisiere_anzeige()
        popup.destroy()

    speichern_button = ctk.CTkButton(popup, text="Speichern", command=speichern)
    speichern_button.pack(pady=20)


def markieren(index):
    todos[index]["Erledigt"] = not todos[index]["Erledigt"]
    speichere_todos()
    aktualisiere_anzeige()

def loeschen(index):
    del todos[index]
    speichere_todos()
    aktualisiere_anzeige()


todos = lade_todos()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

fenster = ctk.CTk()
fenster.title("ToDo - Liste")
fenster.geometry("650x800")
fenster.resizable(False, False)
fenster.iconbitmap(ressource_path("logo.ico"))

eingabe_kasten = ctk.CTkFrame(fenster, corner_radius=12)
eingabe_kasten.pack(pady=(20, 10), padx=20, fill="x")
eingabe_kasten.grid_columnconfigure(0, weight=1)

eingabe = ctk.CTkEntry(eingabe_kasten, width=300, placeholder_text="Neue Aufgabe...")
eingabe.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
eingabe.bind("<Return>", lambda event: hinzufuegen())

eingabe1 = ctk.CTkEntry(eingabe_kasten, width=300, placeholder_text="Beschreibung...")
eingabe1.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="ew")
eingabe1.bind("<Return>", lambda event: hinzufuegen())

kategorie_label = ctk.CTkLabel(eingabe_kasten, text="Kategorien:")
kategorie_label.grid(row=0, column=1, padx=(0, 12), pady=(7.5, 5))

kategorie_var = ctk.StringVar(value="Sonstiges")
kategorie_menu = ctk.CTkOptionMenu(
        eingabe_kasten,
        values=["Python", "C#", "C++", "Java", "JavaScript", "Sonstiges"],
        variable=kategorie_var,
        width=120
        )
kategorie_menu.grid(row=0, column=2, padx=(0, 10), pady=(10, 5))

button_hinzufuegen = ctk.CTkButton(eingabe_kasten, text="Hinzufügen", command=hinzufuegen)
button_hinzufuegen.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

listen = ctk.CTkFrame(fenster, fg_color="transparent")
listen.pack(fill="x", padx=20, pady=(0, 5))

statistic_label = ctk.CTkLabel(listen, text="")
statistic_label.pack(side="left")

kategories_filter_var = ctk.StringVar(value="Ohne Filter")
kategories_filter = ctk.CTkOptionMenu(
    listen,
    values=["Ohne Filter", "Python", "C#", "C++", "Java", "JavaScript", "Sonstiges"],
    variable=kategories_filter_var,
    command=lambda wert: aktualisiere_anzeige()
    )
kategories_filter.pack(side="right")

kategories_filter_label = ctk.CTkLabel(listen, text="Filter:")
kategories_filter_label.pack(side="right", padx=(0, 12))

tabview = ctk.CTkTabview(fenster, width=600, height=400)
tabview.pack(padx=15, fill="both", expand=True)


tabview.add("Aktiv")
tabview.add("Erledigt")

liste_frame_aktiv = ctk.CTkScrollableFrame(tabview.tab("Aktiv"), width=550, height=300)
liste_frame_aktiv.pack(pady=10, padx=10, fill="both", expand=True)

liste_frame_erledigt = ctk.CTkScrollableFrame(tabview.tab("Erledigt"), width=550, height=300)
liste_frame_erledigt.pack(pady=10, padx=10, fill="both", expand=True)

aktualisiere_anzeige()
fenster.mainloop()