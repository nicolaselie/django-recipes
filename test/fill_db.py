from django.contrib.auth.models import User
from recipes.models import Recipe, Category, Source, BakingInfo
from django.core.files import File

def save_file(obj, filepath):
    with open(filepath, 'rb') as f:
        obj.save(f.name, File(f), save=False)

###
# Users
###
admin = User.objects.all()[0]
user = User.objects.filter(username="mathilde")
if user:
    user = user[0]
if not user:
    user = User.objects.create_user("mathilde", "mathilde@localhost", "123456")

###
# Categories
###

desserts = Category(name="Desserts", description="Les desserts...")
desserts.save()

plats = Category(name="Plats", description="Les plats...")
plats.save()

entrees = Category(name="Entrées", description="Les entrées...")
entrees.save()

###
# Recipes
###

recipe = Recipe(title="Cake Olives-Jambon", author=admin,
                preparation_time="20min",
                portion="5-6")
save_file(recipe.small_picture, 'test/cake jambon olives.jpg')
save_file(recipe.big_picture, 'test/ingredients.jpg')
recipe.ingredients = """vin blanc sec: 15cL
huile d'olive: 15cL
oeufs: 4
gruyère rapé: 100g
farine: 250g
levure: 1 paquet
sel: 1 c. à café
dés de jambon: 200g
olives vertes: 200g"""
recipe.content = """Dans un saladier, travailler le vin, l'huile et les oeufs cassés un par un.
Ajouter la farine, le gruyère rapé, la levure et sel. Terminer par le jambon et les olives coupées en 2.
Faire cuire dans un moule à cake beurré et fariné."""
recipe.category = plats
recipe.save()

temp = BakingInfo(type='FO', temperature='190', time="45min")
temp.recipe = recipe
temp.save()

source = Source(name="Nadine")
source.save()
recipe.sources = [source, ]
recipe.save()

###

recipe = Recipe(title="Cannelés Bordelais", author=user,
                preparation_time="45min",
                portion="12 gros cannelés")
save_file(recipe.small_picture, 'test/canneles.jpg')
save_file(recipe.big_picture, 'test/ingredients.jpg')
recipe.hint = """Laisser reposer la préparation pendant au moins une nuit au réfrigérateur pour que les canelés montent bien pendant la cuisson !
Utiliser une bombe de graisse pour graisser les moules plutôt que du beurre."""
recipe.ingredients = """lait: 1L
gousse de vanille: 1
sucre: 500g
beurre: 100g
jaunes d'oeuf: 6
farine: 300g
rhum blanc: 1 verre"""
recipe.content = """Faire bouillir le lait avec la gousse de vanille fendue en deux et le beurre. Laisser infuser et fondre le beurre pendant 15min. Réserver.
Mélanger le sucre et la farine. Ajouter les jaunes d'oeufs.
Retirer la gousse de vanille.
Ajouter petit à petit le lait et le beurre au mélange. Laisser reposer.
Ajouter un verre de rhum blanc au mélange. Remplir les moules au 3/4.
Enfourner 5 min à 275°C. Descendre la température du four à 180°C et laisser cuire pendant 1h. Les cannelés doivent être bien dorés !"""
recipe.category = desserts
recipe.save()

temp = BakingInfo(type='FO', temperature='250', time="1h15min")
temp.recipe = recipe
temp.save()

source = Source(name="Digi")
source.save()
recipe.sources = [source, ]
recipe.save()


###

recipe = Recipe(title="Crêpes Salé-Sucré", author=admin,
                preparation_time="20min",
                portion="12 crêpes")
save_file(recipe.small_picture, 'test/crepes.jpg')
save_file(recipe.big_picture, 'test/ingredients.jpg')
recipe.ingredients = """farine de sarrasin: 100g
farine de blé: 100g
sel: 1/2 cuil. à café
oeufs: 3
lait: 300mL
eau: 300mL
huile: 1 cuil. à soupe
Huile végétale pour la cuisson"""
recipe.content = """Mettre la farine et le sel dans un grand récipient. Ajouter les oeufs un à un et mélanger vigoureusement jusqu'à obtenir une pâte lisse.
Ajouter l'eau, le lait et l'huile. Mélanger vigoureusement jusqu'à obtenir une pâte homogène.
Laisser reposer au minimum 1h. Le mélange s'épaissera légèrement au repos, ajouter alors 3 à 4 cuillerées à soupe d'eau afin de délayer le mélange pour obtenir une pâte ayant la consistance d'une crème un peu épaisse.
Préchauffer la crépière 5min minimum à feu moyen puis huiler la surface avec un peu d'huile végétale.
Verser la valeur d'une petite louche dans la crépière et utiliser le rateau pour étendre la pâte en un mouvement circulaire et former une galette.
Laisser cuire jusqu'à formation de bulles à la surface, décoller alors les bords et retourner la galette à l'aide d'une spatule.
Poser les galettes cuites sur un plat et les couvrir de manière à les conserver au chaud."""
recipe.category = desserts
recipe.save()

source = Source(name="Le Creuset")
source.save()
recipe.sources = [source, ]
recipe.save()