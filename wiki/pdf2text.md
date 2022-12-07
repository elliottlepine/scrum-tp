# Veille technologique pdf2text

## Résumé

pdf2txt extrait le contenu textuel d'un fichier PDF.

Il extrait tout le texte qui doit être rendu de manière rendu de manière programmatique, c'est-à-dire le texte représenté sous forme de chaînes ASCII ou Unicode.

**Il ne peut pas reconnaître le texte dessiné comme des images qui nécessiteraient une reconnaissance optique des caractères.**

Il permet également d'extraire les **emplacements correspondants, les noms de police, les tailles de police, le sens d'écriture (horizontal ou vertical) pour chaque texte**.

Vous devez fournir un mot de passe pour les documents PDF protégés lorsque leur accès est restreint.

Vous ne pouvez pas extraire de texte d'un document document PDF qui n'a pas l'autorisation d'extraction.

## Arguments

### -o

Chemin du fichier de sortie (.txt)

### -p

Liste des pages à extraire

### -t

Type de fichier de sortie

### -M -L -W

Définit la longueur des marges des caractères, des lignes, et des mots.

### -A

Forcer l'analyse de la mise en page, incluant le text figures

### -n

Nombre de pages à extraire

### -P

Mot de passe du fichier, s'il est protégé.

## Points forts

- Reconnaissance de la mise en page
- Reconnaissance du texte des figures

## Limites

- Pas d'images ou de reconaissance d'images
- Pas de tableaux ?

