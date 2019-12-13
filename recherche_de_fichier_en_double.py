#!/usr/bin/python
#coding:utf-8

import os, stat, hashlib
from random import sample
from psutil import virtual_memory

from Tkinter import *
from tkMessageBox import *
from tkFileDialog import *
from PIL import Image, ImageTk

import sys
reload(sys)
sys.setdefaultencoding('utf8')

###### Initialisation des paramètres :
print "Starting program..."
program_path = os.getcwd()
# Fonction qui va regénérer les paramètres si besoin
def creation_config_file() :
    print "Création du fichier de configuration..."
    config_file = open(program_path + "/recherche_double_fichier.conf", 'w')
    config_file.write("""
## SYNTAXE UTILISE ##

# - Les Liste des formats se trouve sur deux seules lignes (fichier modifiable, et non modifiable) ; seul les exensions sont mise sur la ligne et rangés de cette manière : [.extension, .extension, .extension] →ne pas mettre de  à la fin de la ligne, ni au début
# - Les paramètres sont les derniers choix de traitement que vous avez utilisé.


## LISTE DES FORMATS MODIFIABLE FACILEMENT OU PAS ##

# Facilement modifiable (fichier txt, word, etc...). Il est possible que vous soyez ammenés à les renommer afin dêtre avertis du lien à un autre chemin vers se même fichier.
.txt, .docx, .odt, .odp, .pptx, .odg, .xcf, .py, .svg, .xls

# Dificilement modifiable (multimédia, etc...). Vous ne voudrez peut-être pas que les musiques (par exemple) soit renommé en ajoutant  - (fichier lié) à la fin du nom :
.pdf, .jpg, .jpeg, .png, .gif, .tif, .mp3, .ogg, .3gp, .flv, .flac, .wav, .wma, .mp4, .avi, .mkv, .tmp, .html, .htm, .zip, .f4f, .rtf, .php, .cgi, .rar, .nfo, .xpi, .pset, .exp, .profile, .xiti, .js, .css, .ui 


## PARAMETRES DE TRAITEMENT ##

# Supression et création de lien pour les fichiers en double : (deux valeurs possibles : all/limited/none)
limited

# Renommage de quels fichiers : (trois valeurs possibles : all/limited/none)
all

# Taille maximum autorisé a étre ouvert dans la RAM (en Mo) :
1000

# Dernier dossier ouvert


## ATTENTION : ##
# Vous pouvez modifier se fichier, mais si vous ne respectez pas la syntaxe utilisé, le fichier sera supprimé lors de lutilisation du logiciel.
# N'ajoutez a aucun moment un saut de ligne. Cela rendra le fichier illisible.""")
    config_file.close()

# Vérification des anciens paramètres
if os.path.exists(program_path + "/recherche_double_fichier.conf") and os.path.getsize(program_path + "/recherche_double_fichier.conf") < 1600 :
    creation_config_file()
# Créations de nouveau paramètre si inexistanr
if not os.path.exists(program_path + "/recherche_double_fichier.conf") : creation_config_file()

# Ouverture des paramètres
config_file = open(program_path + "/recherche_double_fichier.conf", 'r')
configuration = config_file.readlines()
config_file.close()

# Si le fichier n'a pas le bon nombre de ligne : erreur, on le recréer
if len(configuration) != 33 :
    creation_config_file()
    # On réouvre le fichier
    config_file = open(program_path + "/recherche_double_fichier.conf", 'r')
    configuration = config_file.readlines()
    config_file.close()

editable_file_list = configuration[10].split(", ")
editable_file_list[0] = editable_file_list[0]
editable_file_list[len(editable_file_list)-1] = editable_file_list[len(editable_file_list)-1][:-1]

uneditable_file_list = configuration[13].split(", ")
uneditable_file_list[0] = uneditable_file_list[0]
uneditable_file_list[len(uneditable_file_list)-1] = uneditable_file_list[len(uneditable_file_list)-1][:-1]

try : config_taill_max = int(configuration[25][:-1])
except : config_taill_max = 1000

if os.path.exists(configuration[28][:-1]) : chemin_repertoire = configuration[28][:-1]
else : chemin_repertoire = os.environ["HOME"]




def parametre() :
    def ajout_des_parametres() :
        global configuration
        global editable_file_list
        global uneditable_file_list
        global chemin_repertoire
        global config_taill_max

        for ext in editable_file_list :
            liste_renommable.insert(END, ext)
        for ext in uneditable_file_list :
            liste_non_renommable.insert(END, ext)

        variable_remplacement.set(configuration[19][:-1])
        variable_renommement.set(configuration[22][:-1])
        chemin_dernier_repertoire.set(chemin_repertoire)
        variable_taille_max.delete(0, END)
        variable_taille_max.insert(END, config_taill_max)


    def renommable(action) :
        global editable_file_list

        if action == "remove" :
            index_selection = liste_renommable.curselection()
            liste_renommable.delete(index_selection)

        elif action == "append" :
            erreur_ajout = False
            extension = variable_extensions_renommable.get()

            if extension[0] != "." or len(extension) <=2 :
                showerror("erreur extension", "Erreur : votre extension n'est pas valide.")
                erreur_ajout = True
            elif extension in liste_renommable.get(0, liste_renommable.size()) :
                showerror("erreur extension", "Erreur : L'extension est déjà référencé.")
                erreur_ajout = True
            elif extension in liste_non_renommable.get(0, liste_non_renommable.size()) :
                showerror("erreur extension", "Erreur : L'extension est référencé dans la liste des non renommables.")
                erreur_ajout = True

            if not erreur_ajout :
                editable_file_list.append(extension)


    def non_renommable(action) :
        global uneditable_file_list

        if action == "remove" :
            index_selection = liste_non_renommable.curselection()
            liste_non_renommable.delete(index_selection)

        elif action == "append" :
            erreur_ajout = False
            extension = variable_extensions_non_renommable.get()

            if extension[0] != "." or len(extension) <=2 :
                showerror("erreur extension", "Erreur : votre extension n'est pas valide.")
                erreur_ajout = True
            elif extension in liste_non_renommable.get(0, liste_non_renommable.size()) :
                showerror("erreur extension", "Erreur : L'extension est déjà référencé.")
                erreur_ajout = True
            elif extension in liste_renommable.get(0, liste_renommable.size()) :
                showerror("erreur extension", "Erreur : L'extension est référencé dans la liste des renommables.")
                erreur_ajout = True

            if not erreur_ajout :
                uneditable_file_list.append(extension)


    def enregitrer(action) :
        global configuration
        global chemin_repertoire
        global editable_file_list
        global uneditable_file_list
        global config_taill_max

        editable_file_list = liste_renommable.get(0, liste_renommable.size())
        uneditable_file_list = liste_non_renommable.get(0, liste_non_renommable.size())
        conf_supression = variable_remplacement.get()
        conf_renommage = variable_renommement.get()
        config_taill_max = variable_taille_max.get()

        if os.path.exists(chemin_dernier_repertoire.get()) : chemin_repertoire = chemin_dernier_repertoire.get()

        editable_file = ", ".join(editable_file_list) + "\n"
        uneditable_file = ", ".join(uneditable_file_list) + "\n"

        print editable_file[:-1]
        print uneditable_file[:-1]
        print conf_supression
        print conf_renommage
        print config_taill_max
        print chemin_repertoire

        configuration[10] = editable_file
        configuration[13] = uneditable_file
        configuration[19] = conf_supression + "\n"
        configuration[22] = conf_renommage + "\n"
        configuration[25] = str(config_taill_max) + "\n"
        configuration[28] = chemin_repertoire + "\n"

        config_file = open(program_path + "/recherche_double_fichier.conf", 'w')
        print program_path + "/recherche_double_fichier.conf"

        for line in configuration :
            config_file.write(str(line))
        config_file.close()

        print "saving parameter..."

        if configuration[19] == "all\n" : remplacage_all.select()
        elif configuration[19] == "limited\n" : remplacage_lim.select()
        elif configuration[19] == "none\n" : remplacage_non.select()

        if configuration[22] == "all\n" : renommage_all.select()
        elif configuration[22] == "limited\n" : renommage_lim.select()
        elif configuration[22] == "none\n" : renommage_non.select()

        champ_chemin_repertoire.delete(0.0, END)
        if chemin_repertoire != os.environ["HOME"] : champ_chemin_repertoire.insert(END, chemin_repertoire)
        else : champ_chemin_repertoire.insert(END, " Choisissez un répertoire !")

        if action == "quitter" :
            fenetre_conf.destroy()



    fenetre_conf = Toplevel(fenetre)
    fenetre_conf.title("configuration")

    cadre_principale = Frame(fenetre_conf)
    cadre_principale.grid(row=1, column=3, padx=9, pady=9)

    # Editable file :
    cadre_renommable = LabelFrame(cadre_principale, text=" Fichiers modifiable facilement ")
    cadre_renommable.grid(row=1, column=3, padx=9, pady=9)

    cadre_action_renommable = Frame(cadre_renommable)
    cadre_action_renommable.grid(row=1, column=3, pady=9)
    Button(cadre_action_renommable, text="Remove", command=lambda : renommable("remove")).grid(row=1, column=1, padx=9)
    Button(cadre_action_renommable, text="Append", command=lambda : renommable("append")).grid(row=1, column=2, padx=9)

    variable_extensions_renommable = StringVar()
    Entry(cadre_renommable, textvariable=variable_extensions_renommable, width=20).grid(row=2, column=3, padx=9)
    variable_extensions_renommable.set("Nouvelle extension")

    #barre_defilement_renommable = Scrollbar(cadre_action_renommable, orient=VERTICAL)#, width=18)
    #barre_defilement_renommable.grid(row=3, column=4, padx=9)
    liste_renommable = Listbox(cadre_renommable)#, yscrollcommand=barre_defilement_renommable.set)
    liste_renommable.grid(row=3, column=3, padx=9, pady=9)
    #barre_defilement_renommable.config(command=liste_renommable.yview)


    # Uneditable file :
    cadre_non_renommable = LabelFrame(cadre_principale, text=" Fichiers non modifiable ")
    cadre_non_renommable.grid(row=1, column=5, padx=9, pady=9)

    cadre_action_non_renommable = Frame(cadre_non_renommable)
    cadre_action_non_renommable.grid(row=1, column=3, pady=9)
    Button(cadre_action_non_renommable, text="Remove", command=lambda : non_renommable("remove")).grid(row=1, column=1, padx=9)
    Button(cadre_action_non_renommable, text="Append", command=lambda : non_renommable("append")).grid(row=1, column=2, padx=9)

    variable_extensions_non_renommable = StringVar()
    Entry(cadre_non_renommable, textvariable=variable_extensions_non_renommable, width=20).grid(row=2, column=3, padx=9)
    variable_extensions_non_renommable.set("Nouvelle extension")

    liste_non_renommable = Listbox(cadre_non_renommable)
    liste_non_renommable.grid(row=3, column=3, padx=9, pady=9)


    # Autre paramètres
    cadre_other_parameter = Frame(cadre_principale)
    cadre_other_parameter.grid(row=1, column=7, padx=9, pady=9)

    Label(cadre_other_parameter, text="\n [1] Fichiers à remplacer :").grid(row=1, column=3, padx=9)
    variable_remplacement = StringVar()
    OptionMenu(cadre_other_parameter, variable_remplacement, "all","limited","none").grid(row=2, column=3, padx=9, pady=9)

    Label(cadre_other_parameter, text="\n\n [2] Fichiers à renommer :").grid(row=3, column=3, padx=9)
    variable_renommement = StringVar()
    OptionMenu(cadre_other_parameter, variable_renommement, "all","limited","none").grid(row=4, column=3, padx=9, pady=9)

    Label(cadre_other_parameter, text="\n\n Taille max des fichiers analysés (Mo) :").grid(row=5, column=3, padx=9)
    variable_taille_max = Spinbox(cadre_other_parameter, from_=100, to=10000, increment=10, width=10)
    variable_taille_max.grid(row=6, column=3, padx=9)

    Label(cadre_other_parameter, text="\n\n Dernier chemin ouvert :").grid(row=7, column=3, padx=9)
    chemin_dernier_repertoire = StringVar()
    Entry(cadre_other_parameter, textvariable=chemin_dernier_repertoire, width=30).grid(row=8, column=3, padx=9)


    ajout_des_parametres()


    # Type d'action à réaliser
    texte = """
    - ALL : [1] Tout les fichiers sont remplacés par un lien                                
                          [2] Tout les fichiers remplacés sont renommés en ajoutant : - (fichier lié)\n
    - LIMITED : [1] Seul les fichiers non-modifiable sont remplacés par un lien
                 [2] Seul les fichier modifiable sont renommés                     \n
     - NONE : [1] et [2] Aucun fichiers n'est remplacés ni renommés                 
    """
    champ_definition = Label(fenetre_conf, text=texte)
    # Affichage du label dans la fenêtre
    champ_definition.grid(row=2, column=3, padx=9)



    # Bouton enregistrer
    cadre_bouton = Frame(fenetre_conf)
    cadre_bouton.grid(row=3, column=3, padx=9, pady=9)

    Button(cadre_bouton, text=" Enregistrer ", command=lambda : enregitrer("seul")).grid(row=1, column=2, padx=9)
    Button(cadre_bouton, text="Enregistrer & fermer", command=lambda : enregitrer("quitter")).grid(row=1, column=3, padx=9)
    Button(cadre_bouton, text=" Annuler ", command=fenetre_conf.destroy).grid(row=1, column=4, padx=9)


    fenetre_conf.mainloop()




###### Fenetre qui affiche les infos utile a savoir :
def info():
    # Création de la fenetre
    fen = Toplevel(fenetre)
    fen.title("Information")
    fen.resizable(0,0)
#    fen.geometry("419x380")

    # Définition du texte à afficher
    texte = """
 * Si l'utilisateur choisis de supprimer les fichiers en double,
 les fichiers sont remplacés pas un lien physique. C'est à dire
 que le chemin existe et fonctionne toujours, mais n'est pas
 indépendant des autres fichiers.

 • Sa permet de :
  - Diminuer la place utilisé par les documents
  - Les laisser accessible et modifiable à partir des chemins
 dans lesquels ils sont rangés.
  - De rester indépendant si l'un des chemins est supprimé

 * Vous avez le choix si vous voulez renommer des fichiers.
 • Sa permet de prévenir lorsqu'un fichier est lié à un autre.
 Mais l'on peut aussi choisir de ne pas renommer les fichiers
 non modifiable afin que, par exemple, une musique garde son
 nom d'origine. Il n'est pas utile de savoir qu'elle est lié
 à un autre.


 * Le résultat de la recherche se trouve dans un fichier texte,
 dans le répertoire que vous avez comparé.

 NB : Si il n'y a pas ce fichier, c'est qu'il n'y a aucun fichier en double.
"""

    # Définition de la zone de texte
    champ_info = Label(fen, text = texte)
    champ_info.pack()

    # Définition du bouton quitter (Le programme)
    bouton_quitter = Button(fen, text="Quitter", command=fenetre.quit)
    bouton_quitter.pack(side=LEFT)

    # Définition du bouton Fermer (juste la fenêtre Info)
    bouton_ok = Button(fen, text="Fermer", command=fen.destroy)
    bouton_ok.pack(side=RIGHT)




###### Fonction qui ouvre les répertoires à synchroniser
def ouverture_chemin():
    global chemin_repertoire
    # On définit le chemin initial
    if chemin_repertoire != "\n" and os.path.exists(chemin_repertoire) : chemin_initial = chemin_repertoire
    else : chemin_initial = os.environ["HOME"]
    # On ouvre le chemin
    directory_path = askdirectory(initialdir=chemin_initial)

    # On affiche le chemin si l'utilisateur en a ouvert un
    if type(directory_path) == tuple or directory_path == "" : pass
    else :
        chemin_repertoire = directory_path
        champ_chemin_repertoire.delete(0.0, END)
        champ_chemin_repertoire.insert(END, chemin_repertoire)
        # Et on enregistre dans les paramètres
        configuration[25] = chemin_repertoire + "\n"




###### Fonction qui va ouvrir le fichier de comparaison :
def ouverture_fichier_texte(chemin_fichier) :
    import subprocess
    # définition du chemin absolue où se trouve le fichier de comparaison
    if chemin_fichier == "" : showerror("Erreur de chemin"," Erreur :  vous n'avez pas renseigné de chemin !")
    print "open " + chemin_fichier + "..."
    if os.path.exists(chemin_fichier):
        try :
            # LINUX
            if sys.platform.startswith('linux'): proc = subprocess.Popen(['xdg-open', chemin_fichier], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # WINDOWS
            elif hasattr(os, 'startfile'):  proc = os.startfile(chemin_fichier)
            # MAC
            elif sys.platform == 'darwin': proc = subprocess.Popen(['open', '--', chemin_fichier], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # NON-CONNUS
            else : showerror("Erreur lors de la lecture", " Erreur : Une erreur est survenue lors de la lecture...")

        except : showerror("Erreur lors de la lecture", " Erreur : Une erreur est survenue lors de la lecture...")
        return proc

    else :
        showerror("Erreur d'existance"," Erreur :  le fichier de comparaison n'existe pas...")



# On vérifie que les paramètres sont cohérants et on lance la fonction
def verification() :
    # Lecture des derniers paramètres
    global chemin_repertoire
    type_remplacement_fichier = remplacage.get()
    fichier_a_renommer = renommage.get()

    erreur_choix = False
    erreur_repertoire = False
    erreur_ecriture = False

    # On s'assure des choix de l'utilisateur
    if type_remplacement_fichier == "all" and fichier_a_renommer == "none" :
        if not askyesno("Choix renommage", "Etes vous sûr de ne pas renommer les fichiers remplacé par un lien ?") : erreur_choix = True
    elif type_remplacement_fichier == "all" and fichier_a_renommer == "all" :
        if not askyesno("Choix renommage", "Etes vous sûr de vouloir renommer tous les fichiers remplacé par un lien ?") : erreur_choix = True

    if chemin_repertoire == "" :
        erreur_repertoire = False
        showerror("Erreur répertoire", "Erreur : Vous n'avez pas choisie de répertoire.")
    elif not erreur_choix and not os.path.exists(chemin_repertoire) :
        erreur_repertoire = False
        showerror("Erreur répertoire", "Erreur : Le répertoire que vous avez choisis n'existe pas.")

    # Test des droits d'écriture et de création de lien
    try:
        fichier_test_ecriture = open("test ecriture.tmp",'w') ; fichier_test_ecriture.close()
        os.link("test ecriture.tmp","test création lien.tmp") ; os.remove("test ecriture.tmp") ; os.remove("test création lien.tmp")
    except:
        try : os.remove("test ecriture.tmp")
        except : showerror("erreur de droit", " Erreur :\n - Le programme n'a pas les droit suffisant pour s'exécuter.") ; erreur_ecriture = True

        if erreur_ecriture == False :
            erreur_ecriture = True
            if askyesno("erreur de droit", "Erreur : Les liens ne peuvent pas être créé sur se système de fichier, voulez-vous continuer quand même ?") :
                erreur_ecriture = False
                type_remplacement_fichier = False

    if not erreur_choix and not erreur_repertoire and not erreur_ecriture :
#        try :
        traitement_fichiers(chemin_repertoire, type_remplacement_fichier, fichier_a_renommer)
#        except : showerror("Erreur traitement", "Erreur : Une erreur inconnue est survenue lors du traitement des fichiers")




def traitement_fichiers(chemin_repertoire, remplacer_fichier, renommage) :
    global editable_file_list, uneditable_file_list
    global config_taill_max
###### Mise en place des éléments qui vont être utilisés durant la comparaison

    # Création du fichier dans lequel les fichiers en double (et les erreurs) seront noté : fichier_comparaison
    os.chdir(chemin_repertoire)
    fichier_comparaison = open("Recherche fichier en double.tmp",'w')
    fichier_comparaison = open("Recherche fichier en double.tmp",'a')
#    fichier_comparaison.write("\n INFO : Les fichiers en plusieurs exemplaires sont supprimés et remplacés par un lien physique, pointant vers le documents correspondant !!")
#    fichier_comparaison.write("\n ------------------------------------------------------------------------------------------------------------------------------------------\n\n")

    # On créer des chaines de caractères pour lister les fichiers trop lourd ou non-lisible : texte_fichier_trop_lourd ; texte_fichier_nonlisible
    texte_fichier_nonlisible = "\n • Fichiers non-lisibles :\n" + "   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n"
    texte_fichier_nonhashes = "\n • Fichier qui n'ont pas pus être hashés :\n" + "   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n"
    texte_fichier_trop_lourd = "\n • Fichiers qui sont trop lourds :\n" + "   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n"



###### On liste tous les fichiers qui se trouve dans ce répertoire : Liste_fichiers
    champ_texte.config(text = " - Construction de la liste des fichiers du répertoire...\n\n")
    champ_texte.update()

    # Création de la liste des éléments du répertoire :
    Liste_fichiers_non_trie = []
    Liste_tailles = []

    # Création d'une liste de tri :
    Liste_elements_refuses = [".json",".manifest",".js",".dtd",".ini",".css",".properties",".so","__init__",".loaded_0"]

    # On liste tous les fichiers des dossiers / sous-dossier...
    for dossier, sous_dossiers, fichiers in os.walk(chemin_repertoire):
        for fichier in fichiers:
            document = os.path.join(dossier, fichier)
            # On fait un peu de tri pour les fichiers qu'on retrouve a chaque page web enregistré (inintérressant) :
            ajout = True

            try :
                # Interdiction de fichier nul, de certaine chaine dans les noms de dossier et des liens
                if os.path.getsize(document) == 0 : ajout = False
                elif "_data" in dossier or "_fichier" in dossier or "profile.default" in dossier or "_files" in dossier : ajout = False
                elif os.path.islink(document) : ajout = False

                # Interdiction du fichier si un élément de la liste se trouve dans son nom
                for element in Liste_elements_refuses :
                    if element in fichier : ajout = False

                # Interdiction du fichier si on a pas les droits d'écritures
                try :
                    fichier_test_ecriture = open(document, 'a') ; fichier_test_ecriture.close()
                except IOError :
                    texte_fichier_droit_insuffisant = texte_fichier_droit_insuffisant + " - " + document + "\n"
                    ajout = False

            except : ajout = False

            # Si il n'y a aucune interdiction, on l'ajoute à la liste
            if ajout == True :
                Liste_fichiers_non_trie.append(document)
                Liste_tailles.append(os.path.getsize(document))



###### On Trie rapidement les fichiers qui sont uniques par rapport à leurs taille : Liste_fichier_double_possible
    Liste_fichiers = []
    longueur_liste_taille = len(Liste_tailles)-1
    taille_total_fichiers = 0

    for rang, taille in enumerate(Liste_tailles) :
        champ_texte.config(text = " - Première boucle de trie large : " + str(rang*100/longueur_liste_taille) + " % \n\n")
        champ_texte.update()

        # recherche si la taille reviens plusieurs fois
        nombre_foi_cette_taille = Liste_tailles.count(taille)
        if nombre_foi_cette_taille > 1 :
            Liste_fichiers.append(Liste_fichiers_non_trie[rang])
            taille_total_fichiers += os.path.getsize(Liste_fichiers_non_trie[rang])



###### On créer une liste des hashs des éléments du répertoire : Liste_des_hash
    Liste_des_hash = []
    Liste_des_inodes = []
    longueur_liste = len(Liste_fichiers) -1
    taille_fichier_analyse = 0

    # Boucle de calcul des hashs de tout les fichiers
    for nm_fichier,fichier in enumerate(Liste_fichiers) :
        taille_fichier_analyse += os.path.getsize(fichier)
        texte = " - Avancement des calculs des hashs...\n\n  {0} %   |   {1}/{2}".format(str(taille_fichier_analyse*100/taille_total_fichiers),
                                                                                         str(nm_fichier+1),
                                                                                         str(longueur_liste+1) + chr(13) )
        champ_texte.config(text = texte)
        champ_texte.update()

        # Ajout inode
        inode_fichier = os.stat(fichier)[stat.ST_INO]
        Liste_des_inodes.append(inode_fichier)

        # Si il reste + de 512Mio de mémoire RAM (fichier qui va être hashé inclus), on essais de calculer le hash du fichier
        if os.path.getsize(fichier) <= config_taill_max*1000000 :
            try :
                hash_du_fichier = hashlib.sha256(open(fichier,'rb').read()).hexdigest()
                Liste_des_hash.append(hash_du_fichier)
            except :
                Liste_des_hash.append("".join(sample("azertyuiopsdfgjklmwxcvbn123567890",19)))
                texte_fichier_nonhashes = texte_fichier_nonhashes + "\n - " + fichier
        # Sinon fichier trop lourd
        else :
            texte_fichier_trop_lourd += "\n - " + fichier
            Liste_des_hash.append("".join(sample("azertyuiopsdfgjklmwxcvbn123567890",19)))



###### On écrit dans le fichier les erreurs rencontrées :
    if len(texte_fichier_nonlisible) > 97 : fichier_comparaison.write(texte_fichier_nonlisible + "\n\n")
    if len(texte_fichier_nonhashes) > 163 : fichier_comparaison.write(texte_fichier_nonhashes + "\n\n")
    if len(texte_fichier_trop_lourd) > 129 : fichier_comparaison.write(texte_fichier_trop_lourd + "\n\n")

    texte_fichier_nom_traite = "\n • Fichiers qui n'ont pas pu être traités :\n" + "   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n"



###### On compare les hashs entre eux pour trouver les fichiers identiques
    fichier_comparaison.write("\n • Fichier qui sont en plusieurs exemplaires :\n" + "   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n\n")
    nombre_fichier_double = 0
    Liste_hash_traite = []
    longueur_liste_hash = len(Liste_des_hash)

    for rang_compare in range(longueur_liste_hash) :
        champ_texte.config(text = " - Deuxième boucle de trie fine : " + str(rang_compare*100/longueur_liste_hash) + " % \n\n")
        champ_texte.update()

        hash_compare = Liste_des_hash[rang_compare]
        inode_compare = Liste_des_inodes[rang_compare]
#        print "\n\n compare : " + str(rang_compare) + " ; " + hash_compare + " ; " + str(inode_compare) + "\n"
        # Servira à savoir s'il faut sauter une ligne dans le fichier résultat
        fichier_en_double = False

        if hash_compare in Liste_hash_traite : continue

        for rang_comparant in range(rang_compare+1, longueur_liste_hash) :
            hash_comparant = Liste_des_hash[rang_comparant]
            inode_comparant = Liste_des_inodes[rang_comparant]
#            print str(rang_comparant) + " ; " + hash_comparant + " ; " + str(inode_comparant)

            if hash_compare == hash_comparant and inode_compare != inode_comparant and not hash_comparant in Liste_hash_traite :
                fichier_en_double = True
                nom_compare = Liste_fichiers[rang_compare]
                nom_comparant = Liste_fichiers[rang_comparant]

                # Si on renomme tout
                if remplacer_fichier == "all" and renommage == "all" :
#                    print "ALL | ALL " + str(rang_compare) + "." + str(rang_comparant)
                    if not " - (fichier lié)" in nom_compare :
                        nouveau_nom_compare = os.path.splitext(nom_compare)[0] + " - (fichier lié)" + os.path.splitext(nom_compare)[1]
                    else : nouveau_nom_compare = nom_compare
                    os.rename(nom_compare, nouveau_nom_compare)
                    if not " - (fichier lié)" in nom_comparant :
                        nouveau_nom_comparant = os.path.splitext(nom_comparant)[0] + " - (fichier lié)" + os.path.splitext(nom_comparant)[1]
                    else : nouveau_nom_comparant = nom_comparant
                    os.remove(nom_comparant)
                    os.link(nouveau_nom_compare, nouveau_nom_comparant)


                # Si on créer un lien pour tous les fichiers et qu'on en renomme un partie
                elif remplacer_fichier == "all" and renommage == "limited" :
#                    print "ALL | LIMITED " + str(rang_compare) + "." + str(rang_comparant)
                    extensions_compare = os.path.splitext(nom_compare)[1].lower()
                    extensions_comparant = os.path.splitext(nom_comparant)[1].lower()
                    if len(extensions_compare) <= 2 : extensions_compare = extensions_comparant
                    if len(extensions_comparant) <= 2 : extensions_comparant = extensions_compare

                    # Fichier que l'on renomme
                    if extensions_compare in editable_file_list or extensions_comparant in editable_file_list :
                        if not " - (fichier lié)" in nom_compare :
                            nouveau_nom_compare = os.path.splitext(nom_compare)[0] + " - (fichier lié)" + extensions_compare
                            os.rename(nom_compare, nouveau_nom_compare)
                        else : nouveau_nom_compare = nom_compare
                        if not " - (fichier lié)" in nom_comparant :
                            nouveau_nom_comparant = os.path.splitext(nom_comparant)[0] + " - (fichier lié)" + extensions_comparant
                        else : nouveau_nom_comparant = nom_comparant

                    # Fichier qu'on ne renomme pas
                    elif extensions_compare in uneditable_file_list or extensions_comparant in uneditable_file_list :
                        nouveau_nom_compare = nom_compare
                        nouveau_nom_comparant = nom_comparant

                    # Fichier inconnue, qu'on renomme
                    elif askyesno("Format inconnue", "L'extensions n'est pas connue : " + extensions_compare + "\n Voulez vous renommer ce type de fichier avant de le lier ?") :
                        editable_file_list.append(extensions_compare)
                        if not " - (fichier lié)" in nom_compare :
                            nouveau_nom_compare = os.path.splitext(nom_compare)[0] + " - (fichier lié)" + extensions_compare
                            os.rename(nom_compare, nouveau_nom_compare)
                        else : nouveau_nom_compare = nom_compare
                        if not " - (fichier lié)" in nom_comparant :
                            nouveau_nom_comparant = os.path.splitext(nom_comparant)[0] + " - (fichier lié)" + extensions_comparant
                        else : nouveau_nom_comparant = nom_comparant
                    # qu'on renomme pas
                    else :
                        uneditable_file_list.append(extensions_compare)
                        nouveau_nom_compare = nom_compare
                        nouveau_nom_comparant = nom_comparant

                    os.remove(nom_comparant)
                    os.link(nouveau_nom_compare, nouveau_nom_comparant)


                # Si on ne renomme rien
                elif remplacer_fichier == "all" and renommage == "none" :
#                    print "ALL | NONE " + str(rang_compare) + "." + str(rang_comparant)
                    nouveau_nom_compare = nom_compare
                    nouveau_nom_comparant = nom_comparant
                    os.remove(nom_comparant)
                    os.link(nouveau_nom_compare, nouveau_nom_comparant)


               # Si on ne créer un lien que pour les fichiers certains fichier mais qu'on les renommes
                elif remplacer_fichier == "limited" and renommage == "all" :
#                    print "LIMITED | ALL " + str(rang_compare) + "." + str(rang_comparant)
                    extensions_compare = os.path.splitext(nom_compare)[1].lower()
                    extensions_comparant = os.path.splitext(nom_comparant)[1].lower()
                    # Si c .tar.gz, on enregistre l'extension complète
                    if extensions_compare == ".gz" and nom_compare[-7:] == ".tar.gz" :
                        extensions_compare = ".tar.gz" ; extensions_comparant = ".tar.gz"
                        # On enlève la première extensions (.gz), la deuxième est enlevé après
                        nom_compare = os.path.splitext(nom_compare)[0]
                        nom_comparant = os.path.splitext(nom_comparant)[0]

                    if len(extensions_compare) <= 2 : extensions_compare = extensions_comparant
                    elif len(extensions_comparant) <= 2 : extensions_comparant = extensions_compare

                    # Fichier qu'on ne renomme pas
                    if extensions_compare in uneditable_file_list or extensions_comparant in uneditable_file_list :
                        if not " - (fichier lié)" in nom_compare :
                            nouveau_nom_compare = os.path.splitext(nom_compare)[0] + " - (fichier lié)" + extensions_compare
                            os.rename(nom_compare, nouveau_nom_compare)
                        else : nouveau_nom_compare = nom_compare
                        if not " - (fichier lié)" in nom_comparant :
                            nouveau_nom_comparant = os.path.splitext(nom_comparant)[0] + " - (fichier lié)" + extensions_comparant
                        else : nouveau_nom_comparant = nom_comparant

                        os.remove(nom_comparant)
                        os.link(nouveau_nom_compare, nouveau_nom_comparant)

                    else :
                        nouveau_nom_compare = nom_compare
                        nouveau_nom_comparant = nom_comparant


               # Si on ne créer un lien que pour les fichiers qu'on ne renomme pas
                elif remplacer_fichier == "limited" and renommage == "limited" or remplacer_fichier == "limited" and renommage == "none" :
#                    print "LIMITED | LIMITED/NONE " + str(rang_compare) + "." + str(rang_comparant)
                    extensions_compare = os.path.splitext(nom_compare)[1].lower()
                    extensions_comparant = os.path.splitext(nom_comparant)[1].lower()
                    if len(extensions_compare) <= 2 : extensions_compare = extensions_comparant
                    if len(extensions_comparant) <= 2 : extensions_comparant = extensions_compare

                    nouveau_nom_compare = nom_compare
                    nouveau_nom_comparant = nom_comparant

                    if extensions_compare in uneditable_file_list or extensions_comparant in uneditable_file_list :
                        os.remove(nom_comparant)
                        os.link(nouveau_nom_compare, nouveau_nom_comparant)
                    elif extensions_compare in editable_file_list or extensions_comparant in editable_file_list : pass
                    # Fichier inconnue qu'on va lier (donc non modifiable)
                    elif askyesno("Format inconnue", "L'extensions n'est pas connue : " + extensions_compare + "\n Voulez vous créer un lien avec ce format de fichier ? (il ne sera donc pas renommé)") :
                        uneditable_file_list.append(extensions_compare)
                        os.remove(nom_comparant)
                        os.link(nouveau_nom_compare, nouveau_nom_comparant)
                    else : editable_file_list.append(extensions_compare)


               # Si on ne créer pas de lien
                elif remplacer_fichier == "none" :
                    nouveau_nom_compare = nom_compare
                    nouveau_nom_comparant = nom_comparant


                # Si on ne remplace pas, on ne renomme pas non plus, on marque dans le fichier
                fichier_comparaison.write(" - " + nouveau_nom_comparant + "\n")
                Liste_fichiers[rang_comparant] = nouveau_nom_comparant
                Liste_fichiers[rang_compare] = nouveau_nom_compare
                nombre_fichier_double += 1

        # Si le fichier comparé a eu des doubles, on l'ajoute pcq pas encore fais
        if fichier_en_double :
            Liste_hash_traite.append(hash_compare)
            fichier_comparaison.write(" - " + nouveau_nom_compare + "\n\n\n")
            nombre_fichier_double += 1



###### Enregistrements des éléments qui vont être utilisés durant la comparaison
    # si il n'y en a pas de fichier en double
    if nombre_fichier_double == 0 :
        os.remove("Recherche fichier en double.tmp")
        champ_texte.config(text = "* Comparaison terminée ! Il n'y a aucun fichier en double !!\n\n")

    else :
        os.rename("Recherche fichier en double.tmp","Résultat comparaison double de fichier.txt")
        champ_texte.config(text = " * Comparaison terminée ! Il y a " + str(nombre_fichier_double) + " fichiers identiques.\n\n")
        # On écrit dans le fichier à la fin le nombre de fichier en double
        fichier_comparaison.write("\n\n\n → Il y a " + str(nombre_fichier_double) + " fichier en double.\n\n")

    champ_texte.update()
    fichier_comparaison.close()





###### Fonction qui va enregistrer les paramètres de la dernière utilisation
def fermeture_logiciel() :
    global configuration
    global chemin_repertoire
    global config_taill_max
    global editable_file_list, uneditable_file_list
    conf_supression = remplacage.get()
    conf_renommage = renommage.get()

    editable_file = ", ".join(editable_file_list) + "\n"
    uneditable_file = ", ".join(uneditable_file_list) + "\n"

    print editable_file[:-1]
    print uneditable_file[:-1]
    print conf_supression
    print conf_renommage
    print config_taill_max
    print chemin_repertoire

    configuration[10] = editable_file
    configuration[13] = uneditable_file
    configuration[19] = conf_supression + "\n"
    configuration[22] = conf_renommage + "\n"
    configuration[25] = str(config_taill_max) + "\n"
    configuration[28] = chemin_repertoire + "\n"

    config_file = open(program_path + "/recherche_double_fichier.conf", 'w')
    for line in configuration :
        config_file.write(str(line))
    config_file.close()
    print "program exiting..."

    fenetre.destroy()




###### Fenêtre principal :

# Definition de la fenetre
fenetre = Tk()
fenetre.title("Rechercher des fichiers en double")
fenetre.protocol("WM_DELETE_WINDOW", fermeture_logiciel)
Mon_icone = PhotoImage(file = os.getcwd()+"/icone_recherche_fichier_double.png")
fenetre.tk.call('wm', 'iconphoto', fenetre._w, Mon_icone)
fenetre.resizable(0,0)

# Zone de l'explication du programme :
champ_nom = Label(fenetre, text = "Bienvenus dans le comparateur de fichier !!")
champ_nom.grid(row=1, column=3, pady=9)


# Affichage du bouton INFO et CONFIG :
cadre_info_config = Frame(fenetre, width=900, height=50)
cadre_info_config.grid(row=3, column=3)

#"/usr/share/icons/Adwaita/32x32/apps/user-info.png"
img_open_info = Image.open(os.getcwd()+"/user-info.png")
icon_info = ImageTk.PhotoImage(img_open_info)
Button(cadre_info_config, image=icon_info, command=info).grid(row=2, column=2, padx=9)

#"/usr/share/icons/Adwaita/32x32/emblems/emblem-system-symbolic.symbolic.png"
img_open_config = Image.open(os.getcwd()+"/emblem-system-symbolic.png")
icon_config = ImageTk.PhotoImage(img_open_config)
bouton_config = Button(cadre_info_config, image=icon_config, command=parametre)
bouton_config.grid(row=2, column=4, padx=9)


# Zone de demande d'entrez du chemin !
champ_entre_hash = Label(fenetre, text = "\n\nChemin du répertoire à comparer :")
champ_entre_hash.grid(row=4, column=3)

# Zone d'affichage du chemin du premier répertoire :
#"/usr/share/icons/menta/32x32/actions/gtk-open.png"
img_open_file = Image.open(os.getcwd()+"/gtk-open.png")
icon_file = ImageTk.PhotoImage(img_open_file)
bouton_clean = Button(fenetre, image=icon_file, command=ouverture_chemin)
bouton_clean.grid(row=5, column=2, padx=9)
# zone d'affichage du chemin
champ_chemin_repertoire = Text(fenetre, height=3, width=100, wrap=WORD)
champ_chemin_repertoire.grid(row=5, column=3, pady=9)
if chemin_repertoire != os.environ["HOME"] : champ_chemin_repertoire.insert(END, chemin_repertoire)
else : champ_chemin_repertoire.insert(END, " Choisissez un répertoire !")


# Zone de demande si remplacement_fichier :
cadre_remplacage = LabelFrame(fenetre, text=" Fichiers à lier ")
cadre_remplacage.grid(row=7, column=3, pady=9)

remplacage = StringVar()
remplacage_all = Radiobutton(cadre_remplacage, text = " Remplacer TOUT les fichiers en double par un lien", variable=remplacage, value="all")
remplacage_lim = Radiobutton(cadre_remplacage, text = " Remplacer seulement les fichiers non-modifiables", variable=remplacage, value="limited")
remplacage_non = Radiobutton(cadre_remplacage, text = " Ne remplacer aucun fichier" + " "*33, variable=remplacage, value="none")
remplacage_all.grid(row=1, column=3)
remplacage_lim.grid(row=2, column=3)
remplacage_non.grid(row=3, column=3)

if configuration[19] == "all\n" : remplacage_all.select()
elif configuration[19] == "limited\n" : remplacage_lim.select()
elif configuration[19] == "none\n" : remplacage_non.select()

# Zone de demande si renommage :
cadre_renommage = LabelFrame(fenetre, text=" Fichiers à renommer ")
cadre_renommage.grid(row=8, column=3, pady=9)

renommage = StringVar()
renommage_all = Radiobutton(cadre_renommage, text = " Renommer tous les fichiers liés en ajoutant : - (fichier lié)", variable=renommage, value="all")
renommage_lim = Radiobutton(cadre_renommage, text = " Renommer seulement les fichiers facilements modifiable", variable=renommage, value="limited")
renommage_non = Radiobutton(cadre_renommage, text = " Ne renommer aucun fichier" + " "*43, variable=renommage, value="none")
renommage_all.grid(row=1, column=3)
renommage_lim.grid(row=2, column=3)
renommage_non.grid(row=3, column=3)

if configuration[22] == "all\n" : renommage_all.select()
elif configuration[22] == "limited\n" : renommage_lim.select()
elif configuration[22] == "none\n" : renommage_non.select()


# Zone de texte pour afficher là ou sa en est :
champ_detail = Label(fenetre, text = "\nDétails des opérations : ")
champ_detail.grid(row=10, column=3)

# Zone de texte réservé pour l'affichage des opérations en cour :
champ_texte = Label(fenetre, text = "\n\n")
champ_texte.grid(row=11, column=3, pady=9)

# Création d'un cadre qui va afficher toute les boutons des actions principales :
cadre = Frame(fenetre, width=900, height=50)
cadre.grid(row=12, column=3, pady=9)

# Affichage du bouton comparer :
bouton_ouvrir = Button(cadre, text="Ouvrir les Résultat", command=lambda : ouverture_fichier_texte(chemin_repertoire + "/Résultat comparaison double de fichier.txt"))
bouton_ouvrir.grid(row=1, column=1)

# Affichage du bouton ouvrir, pour ouvrir le fichier de comparaison
bouton_comparer = Button(cadre, text="Comparer", command=verification)
bouton_comparer.grid(row=1, column=2, padx=19, pady=9)

# Affichage d'un bouton Quitter :
bouton_quitter = Button(cadre, text=" Quitter ", command=fermeture_logiciel)
bouton_quitter.grid(row=1, column=3)


fenetre.mainloop()
