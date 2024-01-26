# Primer Web Scrap 🤖
![Static Badge](https://img.shields.io/badge/Python-3.11.0-green)
![Static Badge](https://img.shields.io/badge/Scrapy-2.11.0-blue)

- Para este ejercicio se realizará un scrap básico a una web de juegos de mesa https://boardgamegeek.com/
- De la lista de todos los juegos de mesa de la web, vamos a adquirir los siguientes datos:
  - Ranking
  - Nombre
  - Año
  - Nota de la página
  - Nota media
  - Número de votos  
- Guardar los datos en un json

## Entorno 💻
- Lo primero de todo es instalar la librería *scrapy* y el módulo de Python *virtualenv*
```python
pip install scrapy

pip install virtualenv
```

- Tras ello, crearemos un entorno virtual para trabajar y lo activaremos
```
py -m venv .venv

.venv\Scripts\activate
```


## Creación del proyecto de scrap y nuestra araña 🕷️
-Tras las instalaciones previas creamos el proyecto base de scrapy
```python
scrapy startproject bgg
```

-Ahora creamos la araña
```python
scrapy genspider bgg https://boardgamegeek.com/
```


## Shell para las comprobaciones previas 🧰	
- Activamos el shell en la consola para las comprobaciones previas
```
scrapy shell
```
- Para este scrap vamos a utilizar *xpath* a la hora de seleccionar las etiquetas html para extraer la información
- Añadimos la ruta donde vamos a hacer las comprobaciones
```
-fetch('https://boardgamegeek.com/browse/boardgame')
```

- Se recibe la respuesta para poder comenzar el scrap
```
response
```
![image](https://github.com/vadillo86/Web-Scrap-/assets/7072809/ff6c6b22-62ff-4262-b690-487dc0e9d7b7)



- Se comprueba si se obtienen todos los elementos de donde queremos extraer los datos
```
response.xpath('//div[@id="collection"]//tr[@id="row_"]')
```
![image](https://github.com/vadillo86/Web-Scrap-/assets/7072809/b1dbc79c-f613-445b-b2fb-c6d6c54f39ad)



- Tras comprobar que obtenemos los elementos correspondientes, se almacena en la variable *games*
```
games = response.xpath('//div[@id="collection"]//tr[@id="row_"]')
```



- Se comprueba el número de elementos que hemos adquirido de la página
```
len(games)
```
![image](https://github.com/vadillo86/Web-Scrap-/assets/7072809/ff6353e3-e8c9-4cca-86e3-e647b08cb9c8)




- Almacenado en la variable, vamos comprobando las rutas de html para adquirir cada dato utilizando en cada ruta
- El primer elemento saltando la cabecera
```
game = games[1]
```
  - Ranking
  ```
  game.xpath('./td[@class="collection_rank"]//a/@name').get()
  ```
![image](https://github.com/vadillo86/Web-Scrap-/assets/7072809/8ae9993e-4b9e-4b10-9bff-4b34928168b7)




- Nombre
```
  game.xpath(f'./td[@id="CEcell_objectname{1}"]//a/text()').get() 
```
![image](https://github.com/vadillo86/Web-Scrap-/assets/7072809/9ee87e15-89c4-46d4-8276-e992f34fc7a6)





- Año
	- Para ello utilizaremos *replace* para adquirir solo el número del año 
	```
	game.xpath(f'./td[@id="CEcell_objectname{1}"]//span[@class="smallerfont dull"]//text()').get()
	.replace("(", "").replace(")", "")
	```
	![image](https://github.com/vadillo86/Web-Scrap-/assets/7072809/cfa80df1-6aef-4e29-8e93-29cb5a17a8e6)




- Dado que las notas vienen las tres juntas, las adquirimos por separado y utilizando *strip* para limpiar caracteres
	- Nota de la página
	```
	game.xpath('./td[@class="collection_bggrating"][1]//text()').get().strip()
	```
 	![image](https://github.com/vadillo86/Web-Scrap-/assets/7072809/32976bf9-c6ee-47fe-be55-c86f7c54a238)



	- Nota media
	```
	game.xpath('./td[@class="collection_bggrating"][2]//text()').get().strip()
	```
	![image](https://github.com/vadillo86/Web-Scrap-/assets/7072809/05f0036a-5664-4710-beb0-9b07125e8838)

 	
	
	- Número de votos
	```
	game.xpath('./td[@class="collection_bggrating"][3]//text()').get().strip()
	```
 	![image](https://github.com/vadillo86/Web-Scrap-/assets/7072809/1d5efba2-335f-42ea-980d-1aeb2e408a8a)




- Tras las comprobaciones corerespondientes y obteniendo la información que necesitamos, se procede a salir del shell
```
exit()
```
- Dado que la nuestra lista de elementos en la web utiliza paginación, se añadirá el código correspondiente
    más adelante para poder scrapear las demás páginas

  

## Programación de la araña en Python 🐍

- Una vez hechas todas las comprobaciones en el shell, es el momento de codificar en código python
- Lo primero de todo será crear la estructura de nuestro item en nuestro clase *item* 
```python
class BggItem(scrapy.Item):
ranking = scrapy.Field()
name = scrapy.Field()
year = scrapy.Field()
rating_geek = scrapy.Field()
rating_avg = scrapy.Field()
num_voters = scrapy.Field()

```

- Ahora importanmos los módulos necesarios y creamos la clase en nuestra clase *bgg.py*
```python
import scrapy
from scrapy import Request
from ..items import BggItem
```

- Lo primero será darle un nombre a nuestra araña e indicarle la url a scrapear.
	También añadiremos un contador para la paginación
```python
class BggSpider(scrapy.Spider):
    name = 'bgg'
    start_urls = ['https://boardgamegeek.com/browse/boardgame/']
    page_count = 1
```

- Después creamos la función para poder recorrer con un bucle cada elemento y así añadirlo al item con cada uno de los datos de cada elemento
```python
    def parse(self, response):
        games_list = response.xpath('//div[@id="collection"]//tr[@id="row_"]')

        for index, game in enumerate(games_list):
            item = BggItem()

            item['ranking'] = game.xpath('./td[@class="collection_rank"]//a/@name').get()
            item['name'] = game.xpath(f'./td[@id="CEcell_objectname{index + 1}"]//a/text()').get()
            item['year'] = game.xpath(f'./td[@id="CEcell_objectname{index + 1}"]//span[@class="smallerfont dull"]//text()').get().replace("(", "").replace(")", "")
            item['rating_geek'] = game.xpath('./td[@class="collection_bggrating"][1]//text()').get().strip()
            item['rating_avg'] = game.xpath('./td[@class="collection_bggrating"][2]//text()').get().strip()
            item['num_voters'] = game.xpath('./td[@class="collection_bggrating"][3]//text()').get().strip()

            yield item
```

- Tras añadir lso datos al item hay que añadir el código para poder hacer la paginación
```python
self.page_count += 1

next_page = f'{self.start_urls[0]}page/{self.page_count}/'
if next_page:
	yield Request(url=next_page, callback=self.parse)
```



- Por último vamos a exportar todos los datos a un json por lo que en la clase *settings.py* se añade lo siguiente
```python
FEEDS = {
    'bggData.jsonl': {'format': 'jsonlines', 'overwrite': False}
}
```

Contodo esto obtenemos un json con todos los elementos y sus datos scrapeados de la web 🥳
