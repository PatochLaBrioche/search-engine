import os
import re
import nltk
import rarfile
from nltk.corpus import stopwords
from zipfile import ZipFile, BadZipFile

# Télécharger les stopwords une fois
nltk.download('stopwords')

# Obtenir les stopwords en français et anglais
stop_words_fr = set(stopwords.words('french'))
stop_words_en = set(stopwords.words('english'))

def nettoyer_sous_titre(fichier_entree, fichier_sortie, extension, encodage='utf-8'):
    try:
        with open(fichier_entree, 'r', encoding=encodage) as fichier:
            lignes = fichier.readlines()

        lignes_nettoyees = []
        dans_section_dialogue = False  # Pour les fichiers .ass

        for ligne in lignes:
            ligne = ligne.strip()

            # Supprimer les balises <i> et </i>
            ligne = re.sub(r'<\/?i>', '', ligne)

            if extension in ['.srt', '.sub', '.vo']:
                # Supprimer les numéros de ligne et les timestamps
                if re.match(r'^\d+$', ligne) or '-->' in ligne or not ligne:
                    continue

                # Pour les fichiers SUB, on supprime les marqueurs de temps {start}{end}
                if extension == '.sub':
                    ligne = re.sub(r'\{.*?\}', '', ligne)
                    # Filtrer les métadonnées (comme "fps" ou "SubEdit")
                    if "fps" in ligne or "SubEdit" in ligne:
                        continue

                # Filtrer les stopwords
                mots = ligne.split()
                mots_filtres = [mot for mot in mots if mot.lower() not in stop_words_fr and mot.lower() not in stop_words_en]
                if mots_filtres:
                    lignes_nettoyees.append(' '.join(mots_filtres))

            elif extension == '.ass':
                # Gestion des fichiers .ass : Ignorer les sections de métadonnées
                if ligne.startswith('[') and 'Events' not in ligne:
                    continue

                # Début de la section "Events"
                if '[Events]' in ligne:
                    dans_section_dialogue = True
                    continue

                # Ignorer les lignes de formatage (Format: ou Style:)
                if not dans_section_dialogue or ligne.startswith('Format:') or ligne.startswith('Style:'):
                    continue

                # Pour les dialogues dans les fichiers .ass, extraire la partie utile après "Dialogue:"
                if ligne.startswith('Dialogue:'):
                    texte = ligne.split(',', 9)[-1]
                    texte = re.sub(r'\{.*?\}', '', texte)  # Supprimer les balises de style (e.g., {\i1}, {\a3}, etc.)
                    texte = texte.replace('\\N', ' ')  # Remplacer les séquences \N par des espaces
                    mots = texte.split()
                    mots_filtres = [mot for mot in mots if mot.lower() not in stop_words_fr and mot.lower() not in stop_words_en]
                    if mots_filtres:
                        lignes_nettoyees.append(' '.join(mots_filtres))

        # Écriture des lignes nettoyées dans le fichier de sortie
        if lignes_nettoyees:
            with open(fichier_sortie, 'w', encoding=encodage) as fichier:
                fichier.write('\n'.join(lignes_nettoyees))

    except UnicodeDecodeError:
        print(f"Erreur de décodage avec l'encodage {encodage}. Essayez un autre encodage.")

def extraire_archive(chemin_archive, dossier_extraction):
    if chemin_archive.lower().endswith('.zip'):
        try:
            with ZipFile(chemin_archive, 'r') as zip_ref:
                zip_ref.extractall(dossier_extraction)
        except BadZipFile:
            print(f"Erreur: {chemin_archive} n'est pas un fichier zip fonctionnel.")
    elif chemin_archive.lower().endswith('.rar'):
        try:
            with rarfile.RarFile(chemin_archive) as rar_ref:
                rar_ref.extractall(dossier_extraction)
        except rarfile.Error:
            print(f"Erreur: {chemin_archive} n'est pas un fichier rar fonctionnel.")

def supprimer_fichiers_et_dossiers_vides(dossier_racine):
    # Supprimer les fichiers .srt, .SRT, .sub, .SUB, .zip, .rar, .vbs, .nfo, .ass, .vo
    extensions_a_supprimer = ('.srt', '.sub', '.zip', '.rar', '.vbs', '.nfo', '.ass', '.vo')
    for sous_dossier, _, fichiers in os.walk(dossier_racine):
        for fichier in fichiers:
            chemin_fichier = os.path.join(sous_dossier, fichier)
            if fichier.lower().endswith(extensions_a_supprimer):
                try:
                    os.remove(chemin_fichier)
                except PermissionError:
                    print(f"Erreur de permission: Impossible de supprimer {chemin_fichier}")

    # Supprimer les dossiers vides
    for sous_dossier, dossiers, _ in os.walk(dossier_racine, topdown=False):
        for dossier in dossiers:
            chemin_dossier = os.path.join(sous_dossier, dossier)
            try:
                os.rmdir(chemin_dossier)
            except OSError:
                pass

def traiter_tous_les_srt(dossier_racine, encodage='utf-8'):
    # Traiter tous les fichiers .srt, .SRT, .sub, .SUB, .vo, .VO, .ass, .ASS, .zip, .rar
    extensions_a_traiter = ('.srt', '.sub', '.vo', '.ass')
    for sous_dossier, _, fichiers in os.walk(dossier_racine):
        for fichier in fichiers:
            chemin_fichier = os.path.join(sous_dossier, fichier)
            extension = os.path.splitext(fichier)[1].lower()
            if extension in extensions_a_traiter:
                fichier_entree = chemin_fichier
                fichier_sortie = os.path.join(sous_dossier, fichier.rsplit('.', 1)[0] + '_nettoye.txt')
                nettoyer_sous_titre(fichier_entree, fichier_sortie, extension, encodage)
            elif extension in ['.zip', '.rar']:
                dossier_extraction = os.path.join(sous_dossier, fichier.rsplit('.', 1)[0])
                os.makedirs(dossier_extraction, exist_ok=True)
                extraire_archive(chemin_fichier, dossier_extraction)
                traiter_tous_les_srt(dossier_extraction, encodage)

    supprimer_fichiers_et_dossiers_vides(dossier_racine)

def fusionner_txt(dossier_racine):
    # Fusionner tous les fichiers .txt dans chaque sous-dossier et les placer à la racine
    for serie in os.listdir(dossier_racine):
        chemin_serie = os.path.join(dossier_racine, serie)
        
        if os.path.isdir(chemin_serie):
            contenu_fusionne = ""
            fichiers_a_supprimer = []
            
            for racine, sous_dossiers, fichiers in os.walk(chemin_serie):
                fichiers_txt = [f for f in fichiers if f.endswith('.txt')]
                
                for fichier_txt in fichiers_txt:
                    chemin_fichier = os.path.join(racine, fichier_txt)
                    with open(chemin_fichier, 'r', encoding='latin1') as f_entree:
                        contenu_fusionne += f_entree.read() + '\n'
                    fichiers_a_supprimer.append(chemin_fichier)

            if contenu_fusionne:
                fichier_sortie = os.path.join(dossier_racine, f'{serie}.txt')
                with open(fichier_sortie, 'w', encoding='utf-8') as f_sortie:
                    f_sortie.write(contenu_fusionne)
                print(f'Fichier fusionné pour la série "{serie}" créé: {fichier_sortie}')
                
                for fichier in fichiers_a_supprimer:
                    os.remove(fichier)
                print(f'Fichiers originaux pour la série "{serie}" supprimés.')
            else:
                print(f'Pas de fichiers .txt trouvés pour la série "{serie}".')

# Utilisation
dossier_racine = './sous-titres'
traiter_tous_les_srt(dossier_racine, encodage='latin1')

fusionner_txt(dossier_racine)

supprimer_fichiers_et_dossiers_vides(dossier_racine)
