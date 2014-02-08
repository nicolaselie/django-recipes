# -*- coding: UTF-8 -*-

from django.contrib.auth.models import User
from recipes.models import Recipe, Category, Source, BakingInfo
from django.core.files import File

import datetime

def save_file(obj, filepath):
    '''Helper to upload files programmatically'''
    with open(filepath, 'rb') as f:
        obj.save(f.name, File(f), save=False)

###
# Users
###
admin = User.objects.all()[0]
user = User.objects.filter(username="user")
if user:
    user = user[0]
if not user:
    user = User.objects.create_user("user", "user@localhost", "123456")

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
save_file(recipe.picture, 'test/cake jambon olives.jpg')
recipe.ingredients = u"""- vin blanc sec: 15cL
- huile d'olive: 15cL
- oeufs: 4
- gruyère rapé: 100g
- farine: 250g
- levure: 1 paquet
- sel: 1 c. à café
- dés de jambon: 200g
- olives vertes: 200g"""
recipe.content = u"""- Dans un saladier, travailler le vin, l'huile et les oeufs cassés un par un.
- Ajouter la farine, le gruyère rapé, la levure et sel. Terminer par le jambon et les olives coupées en 2.
- Faire cuire dans un moule à cake beurré et fariné."""
recipe.category = plats
recipe.cost = 1
recipe.difficulty = 1
recipe.save()

temp = BakingInfo(type=BakingInfo.FAN_OVEN, temperature='190', time="00:45:00")
temp.recipe = recipe
temp.save()

source = Source(name="Nadine")
source.save()
recipe.sources = [source, ]
recipe.save()

date = datetime.datetime.now() - datetime.timedelta(days=30)
Recipe.objects.filter(pk=recipe.pk).update(creation_time=date,
              modification_time=date)

###

recipe = Recipe(title="Cannelés Bordelais", author=user,
                preparation_time="00:45:00",
                portion="12 gros cannelés")
save_file(recipe.picture, 'test/canneles.jpg')
recipe.hint = u"""Laisser reposer la préparation pendant au moins une nuit au réfrigérateur pour que les canelés montent bien pendant la cuisson !
Utiliser une bombe de graisse pour graisser les moules plutôt que du beurre."""
recipe.ingredients = """- lait: 1L
- gousse de vanille: 1
- sucre: 500g
- beurre: 100g
- jaunes d'oeuf: 6
- farine: 300g
- rhum blanc: 1 verre"""
recipe.content = u"""- Faire bouillir le lait avec la gousse de vanille fendue en deux et le beurre. Laisser infuser et fondre le beurre pendant 15min. Réserver.
- Mélanger le sucre et la farine. Ajouter les jaunes d'oeufs.
- Retirer la gousse de vanille.
- Ajouter petit à petit le lait et le beurre au mélange. Laisser reposer.
- Ajouter un verre de rhum blanc au mélange. Remplir les moules au 3/4.
- Enfourner 5 min à 275°C. Descendre la température du four à 180°C et laisser cuire pendant 1h. Les cannelés doivent être bien dorés !"""
recipe.category = desserts
recipe.cost = 2
recipe.difficulty = 3
recipe.save()

temp = BakingInfo(type=BakingInfo.FAN_OVEN, temperature='250', time="01:15:00")
temp.recipe = recipe
temp.save()

source = Source(name="Digi")
source.save()
recipe.sources = [source, ]
recipe.save()

date = datetime.datetime.now() - datetime.timedelta(weeks=1)
Recipe.objects.filter(pk=recipe.pk).update(creation_time=date,
              modification_time=date)


###

recipe = Recipe(title="Crêpes Salé-Sucré", author=admin,
                preparation_time="00:20:00",
                portion="12 crêpes")
save_file(recipe.picture, 'test/crepes.jpg')
recipe.ingredients = u"""- farine de sarrasin: 100g
- farine de blé: 100g
- sel: 1/2 cuil. à café
- oeufs: 3
- lait: 300mL
- eau: 300mL
- huile: 1 cuil. à soupe
- Huile végétale pour la cuisson"""
recipe.content = u"""- Mettre la farine et le sel dans un grand récipient. Ajouter les oeufs un à un et mélanger vigoureusement jusqu'à obtenir une pâte lisse.
- Ajouter l'eau, le lait et l'huile. Mélanger vigoureusement jusqu'à obtenir une pâte homogène.
- Laisser reposer au minimum 1h. Le mélange s'épaissera légèrement au repos, ajouter alors 3 à 4 cuillerées à soupe d'eau afin de délayer le mélange pour obtenir une pâte ayant la consistance d'une crème un peu épaisse.
- Préchauffer la crépière 5min minimum à feu moyen puis huiler la surface avec un peu d'huile végétale.
- Verser la valeur d'une petite louche dans la crépière et utiliser le rateau pour étendre la pâte en un mouvement circulaire et former une galette.
- Laisser cuire jusqu'à formation de bulles à la surface, décoller alors les bords et retourner la galette à l'aide d'une spatule.
Poser les galettes cuites sur un plat et les couvrir de manière à les conserver au chaud."""
recipe.category = desserts
recipe.cost = 1
recipe.difficulty = 1
recipe.save()

source = Source(name="Le Creuset")
source.save()
recipe.sources = [source, ]
recipe.save()

###

recipe = Recipe(title="Macarons au carambar", author=user,
                preparation_time="00:15:00",
                portion="4 personnes")
save_file(recipe.picture, 'test/macarons.jpg')
recipe.hint = """Il est possible de colorer la pâte des coques avec quelques gouttes de colorant alimentaire. Parfois ma garniture est trop "dure", je la repasse quelques secondes au micro-ondes pour la ramollir un peu."""
recipe.ingredients = u"""Pour les coques de macaron :
- 2 blancs d'oeuf (70g environ)
- 85g de poudre d'amandes (fine de préférence)
- 115g de sucre glace
- 50g de sucre en poudre
- 1 cuillère à café de Ricorée ou de cacao en poudre (pour la coloration)

Pour la garniture :
- 50 ml de crème fraiche liquide
- 50g de chocolat blanc
- 10 Carambars"""
recipe.content = u"""Pour les coques :
- Mixer le sucre glace avec la poudre d'amandes et la Ricoré (ou le cacao en poudre), puis passer au chinois pour obtenir une poudre fine.
- Monter les blancs en neige ferme et y incorporer le sucre en poudre.
- Incorporer le mélange sec dans les blancs d'oeufs.
- Former les macarons sur une plaque recouverte de papier sulfurisé, à l'aide d'une poche à douille.
- Laisser crouter 1h puis cuire pendant 15-20 min à 150°.

Pour la garniture :
- Faire fondre à feu très doux les carambars, le chocolat blanc et la crème liquide.
- Une fois le mélange homogène, le laisser refroidir 2h au frigo.
- Garnir les coques avec une cuillère à café ou la poche à douille."""
recipe.category = desserts
recipe.cost = 3
recipe.difficulty = 4
recipe.save()

source = Source(name="Marmiton", url="http://www.marmiton.org")
source.save()
recipe.sources = [source, ]
recipe.save()

###

recipe = Recipe(title="Bricks de poires aux épices et au foie gras", author=user,
                preparation_time="00:20:00",
                portion="4 personnes")
recipe.hint = """Fondant-croustillant, enntrée dont les saveurs épicées rappellent le marché de Noël de Strasbourg... Et cette alliance démontre que le foie gras n'est pas réservé aux blancs liquoreux, mais qu'il se marie très bien avec les vins rouges.
Conseil vin : rouge d'alsace"""
recipe.ingredients = u"""- 2 poires à chair fine
- 4 tranches de foie gras
- 4 feuilles de brick
- 1 cuillère à soupe de miel
- 1 noix de beurre
- 1 cuillère à café d'épices à pain d'épices
- 15 cl de vin rouge"""
recipe.content = u"""Préparation de la recette :

Eplucher les poires, puis les faire cuire dans le mélange vin rouge, miel et épices pendant 30 min. Elles doivent être fondantes et colorées de tous les côtés.

Les couper en tranches fines, puis les disposer au milieu d'une feuille de brick. Rabattre deux à deux les côtés de la brick de façon à former un pavé carré.

Former 4 pavés, les faire dorer 5 min de chaque côté dans le beurre à feu doux.

Servir chaud, après avoir disposé une tranche de foie gras mi-cuit sur les pavés..."""
recipe.category = entrees
recipe.cost = 4
recipe.difficulty = 1
recipe.save()

recipe.sources = [source, ]
recipe.save()

###

recipe = Recipe(title="Galette des rois normande aux pommes", author=user,
                preparation_time="00:15:00",
                portion="8 personnes")
save_file(recipe.picture, 'test/galette_des_rois_normande_aux_pommes.png')
recipe.hint = """1 fève bien sûr"""
recipe.ingredients = u"""-2 disques de pâte feuilletée
- 1 oeuf pour la dorure
- 4 ou 5 pommes boskoop
- 50 à 80 g sucre selon votre goût
- 50 g de beurre
- 2 cs de Calvados ou liqueur de pommes"""
recipe.content = u"""- Eplucher , évider et couper en grosses lamelles les pommes. Faire revenir les pommes dans une poêle avec le beurre. Saupoudrer de sucre , laisser légèrement caraméliser. Ajouter le Calvados , laisser refroidir.
- Répartir les pommes sur la première pâte feuilletée , déposer la fève. Recouvrir avec la seconde pâte feuilletée. Souder le tour de la galette , cranter pour la déco : j 'ai utilisé le denteleur Demarle.
- Rayer la galette en faisant des dessins. Réfrigérer 1 heure pour que le feuilletage monte mieux.
- Dorer à l 'oeuf battu au pinceau
- Enfourner Th7/210°C 25 minutes environ , baisser à Th6/180°C quand elle est bien levée et dorée.
- Laisser tiédir et badigeonner d 'un sirop de sucre si vous la voulez brillante."""
recipe.category = desserts
recipe.cost = 3
recipe.difficulty = 2
recipe.save()

source = Source(name="750g", url="http://www.750g.com/")
source.save()
recipe.sources = [source, ]
recipe.save()