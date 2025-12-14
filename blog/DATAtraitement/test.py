import django_setup
django_setup.setup_django()

from blog.models import *
import pandas as pd

def rechercher_da(code_da):
    """
    Recherche toutes les informations liées à un code DA.
    Crée une ligne pour chaque combinaison Article-ISE.
    """
    try:
        da_obj = DA.objects.filter(id_DA=code_da).first()
        
        if not da_obj:
            print(f"❌ Aucun DA trouvé avec le code: {code_da}")
            return None
        
        relations_da = Appartenir_A_D.objects.filter(da=da_obj).select_related(
            'article', 'article__famille', 'ise'  # ✅ AJOUT de 'ise'
        )
        
        if not relations_da.exists():
            print(f"⚠️ DA {code_da} trouvé mais aucun article associé")
            return None
        
        cache_ises = {}
        for rel_da in relations_da:
            article = rel_da.article
            code_art = article.code_article

            if code_art not in cache_ises:
                tous_les_ises = list(Appartenir_A_D.objects.filter(
                    article=article,
                    da=da_obj
                ).select_related('ise', 'da').order_by('id'))
                cache_ises[code_art] = tous_les_ises
        
        return cache_ises
    except Exception as e:
        print(f"💥 Erreur lors de la recherche DA: {e}")
        return None

def rechercher_interactif():
    while True:
        print("\n🔍 2. Rechercher par code DA")
        
        code_da = input("\n📝 Entrez le code DA: ").strip()
        
        if code_da:
            result = rechercher_da(code_da)
            
            if result:
                print(f"\n✅ Résultat pour DA {code_da}:")
                print("=" * 50)
                
                for code_article, liste_ises in result.items():
                    print(f"\n📦 Article: {code_article}")
                    print(f"   Nombre d'ISE: {len(liste_ises)}")
                    
                    for i, rel_da in enumerate(liste_ises, 1):
                        # ✅ CORRECTION: rel_da est un Appartenir_A_D, pas Appartenir_A_I
                        print(f"   ISE {i}: {rel_da.ise.id_ise if rel_da.ise else 'N/A'} - Qté DA: {rel_da.quantite_DA}")  # ✅ quantite_DA
                
                print("=" * 50)
            else:
                print("❌ Aucun résultat")
        else:
            print("⚠️ Code DA vide")
        
        continuer = input("\n🔄 Continuer? (o/n): ").strip().lower()
        if continuer != 'o':
            break

if __name__ == "__main__":
    rechercher_interactif()