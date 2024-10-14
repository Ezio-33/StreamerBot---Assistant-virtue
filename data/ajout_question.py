import sqlite3
import uuid
from datetime import datetime

def generer_uuid():
    return str(uuid.uuid4())

def inserer_donnees():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    questions_reponses = [
        ("Comment activer AI_Licia sur mon stream Twitch ?", "Configuration", 
         "Pour activer AI_Licia, connectez-vous à votre compte sur getailicia.com, liez votre compte Twitch, puis activez le bot dans les paramètres de votre chaîne."),
        ("Puis-je personnaliser la voix d'AI_Licia ?", "Personnalisation", 
         "Oui, vous pouvez personnaliser la voix d'AI_Licia. Dans les paramètres, vous trouverez des options pour choisir différentes voix, y compris des voix Pro pour un son plus réaliste."),
        ("Comment AI_Licia interagit-elle avec les viewers ?", "Fonctionnalités", 
         "AI_Licia interagit en répondant aux messages du chat, en posant des questions, en lançant des mini-jeux et en commentant le stream en fonction de vos paramètres."),
        ("Quelle est la différence entre les offres Beta AI_Licia + Flex et Unlimited ?", "Abonnement", 
         "L'offre Flex permet 3 streams par semaine, tandis que l'offre Unlimited offre un accès illimité à AI_Licia et un support prioritaire."),
        ("AI_Licia peut-elle modérer le chat ?", "Modération", 
         "AI_Licia n'est pas conçue comme un outil de modération principal, mais elle peut aider à maintenir une ambiance positive dans le chat et signaler des comportements inappropriés."),
        ("Comment configurer AI_Licia pour qu'elle réagisse à des événements spécifiques du stream ?", "Configuration", 
         "Dans le dashboard d'AI_Licia, vous pouvez définir des déclencheurs personnalisés pour que le bot réagisse à des événements comme les nouveaux abonnés, les dons, ou des moments spécifiques de votre stream."),
        ("Puis-je utiliser AI_Licia avec d'autres bots Twitch ?", "Compatibilité", 
         "Oui, AI_Licia est conçue pour fonctionner en harmonie avec d'autres bots Twitch. Vous pouvez même configurer AI_Licia pour utiliser les commandes d'autres bots."),
        ("Comment AI_Licia apprend-elle à connaître ma communauté ?", "Fonctionnalités", 
         "AI_Licia utilise une mémoire à long terme pour se souvenir des interactions avec les viewers. Elle apprend progressivement les préférences et les habitudes de votre communauté."),
        ("Puis-je créer plusieurs profils pour AI_Licia ?", "Personnalisation", 
         "Oui, vous pouvez créer plusieurs profils pour AI_Licia, chacun avec sa propre personnalité, voix et comportement. Cela vous permet d'adapter AI_Licia à différents types de streams."),
        ("Comment AI_Licia gère-t-elle les langues étrangères ?", "Fonctionnalités", 
         "AI_Licia peut être configurée pour comprendre et répondre dans plusieurs langues. Vous pouvez définir une langue principale et des langues secondaires dans les paramètres."),
        ("Quelle est la latence d'AI_Licia pour répondre aux messages du chat ?", "Performance", 
         "La latence d'AI_Licia est généralement très faible, avec des réponses en quelques secondes. La vitesse exacte peut varier en fonction de la complexité de la requête et de la charge du serveur."),
        ("Comment puis-je intégrer AI_Licia à mon overlay de stream ?", "Intégration", 
         "AI_Licia peut être intégrée à votre overlay via notre API. Vous pouvez afficher ses réponses, son avatar ou d'autres éléments visuels directement sur votre stream."),
        ("AI_Licia peut-elle générer du contenu pour mon stream ?", "Fonctionnalités", 
         "Oui, AI_Licia peut générer du contenu comme des idées de jeux, des défis pour les viewers, ou même des histoires courtes basées sur les thèmes de votre stream."),
        ("Comment configurer AI_Licia pour qu'elle ne parle que lorsque je ne suis pas en train de parler ?", "Configuration", 
         "Dans les paramètres avancés, vous pouvez activer la détection de voix. AI_Licia utilisera alors votre flux audio pour détecter quand vous parlez et évitera de vous interrompre."),
        ("Puis-je limiter les interactions d'AI_Licia à certains moments du stream ?", "Personnalisation", 
         "Oui, vous pouvez définir des plages horaires ou des segments spécifiques de votre stream où AI_Licia sera active ou inactive. Cela se configure dans le planning du dashboard."),
        ("Comment AI_Licia gère-t-elle les informations sensibles ou personnelles ?", "Sécurité", 
         "AI_Licia est programmée pour ne pas partager d'informations personnelles. Elle ne stocke pas de données sensibles et est conçue pour respecter la vie privée des utilisateurs."),
        ("Puis-je utiliser AI_Licia pour des streams de jeux spécifiques ?", "Personnalisation", 
         "Oui, vous pouvez créer des profils AI_Licia spécifiques à certains jeux. Par exemple, un profil pour les jeux de stratégie, un autre pour les FPS, etc., chacun avec des connaissances et un comportement adaptés."),
        ("Comment AI_Licia gère-t-elle les raids et les host sur Twitch ?", "Fonctionnalités", 
         "AI_Licia peut être configurée pour accueillir les raids et les hosts de manière personnalisée. Elle peut saluer les nouveaux viewers et leur présenter votre chaîne de manière interactive."),
        ("Puis-je exporter les données d'interaction d'AI_Licia pour analyse ?", "Analyse", 
         "Oui, le dashboard d'AI_Licia offre des options pour exporter les données d'interaction. Vous pouvez analyser ces données pour mieux comprendre l'engagement de votre communauté."),
        ("Comment puis-je signaler un bug ou suggérer une nouvelle fonctionnalité pour AI_Licia ?", "Support", 
         "Vous pouvez signaler des bugs ou suggérer des fonctionnalités via le forum de la communauté sur getailicia.com ou en contactant directement le support si vous avez un abonnement Unlimited.")
    ]

    for question, categorie, reponse in questions_reponses:
        question_id = generer_uuid()
        reponse_id = generer_uuid()
        liaison_id = generer_uuid()
        date_creation = datetime.now().date()

    
        cursor.execute("""
            INSERT INTO Question (id, texte, categorie, date_creation)
            VALUES (?, ?, ?, ?)
        """, (question_id, question, categorie, date_creation))


        cursor.execute("""
            INSERT INTO Reponse (id, texte, question_id, date_creation)
            VALUES (?, ?, ?, ?)
        """, (reponse_id, reponse, question_id, date_creation))


        cursor.execute("""
            INSERT INTO Liaison_Q_R (id, question_id, reponse_id)
            VALUES (?, ?, ?)
        """, (liaison_id, question_id, reponse_id))

    conn.commit()
    conn.close()

    print("20 questions et réponses supplémentaires insérées avec succès !")

if __name__ == "__main__":
    inserer_donnees()