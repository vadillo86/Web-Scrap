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

- Se comprueba si se obtienen todos los elementos de donde queremos extraer los datos
```
response.xpath('//div[@id="collection"]//tr[@id="row_"]')
```


- Tras comprobar que obtenemos los elementos correspondientes, se almacena en la variable *games*
```
games = response.xpath('//div[@id="collection"]//tr[@id="row_"]')
```

- Se comprueba el número de elementos que hemos adquirido de la página
```
len(games)
```


- Almacenado en la variable, vamos comprobando las rutas de html para adquirir cada dato utilizando en cada ruta
	- El primer elemento saltando la cabecera
	```
	game = games[1]
	```
  - Ranking
  ```
  game.xpath('./td[@class="collection_rank"]//a/@name').get()
  ```
  
	- Nombre
	```
  game.xpath(f'./td[@id="CEcell_objectname{1}"]//a/text()').get()  
	```

  - Año
    - Para ello utilizaremos *replace* para adquirir solo el número del año 
    ```
    game.xpath(f'./td[@id="CEcell_objectname{1}"]//span[@class="smallerfont dull"]//text()').get()
    .replace("(", "").replace(")", "")
    ```
    
  - Dado que las notas vienen las tres juntas, las adquirimos por separado y utilizando *strip* para limpiar caracteres
    - Nota de la página
    ```
    game.xpath('./td[@class="collection_bggrating"][1]//text()').get().strip()
    ```
  
    - Nota media
    ```
    game.xpath('./td[@class="collection_bggrating"][2]//text()').get().strip()
    ```
  
    - Número de votos
    ```
    game.xpath('./td[@class="collection_bggrating"][3]//text()').get().strip()
    ```


- Tras las comprobaciones corerespondientes y obteniendo la información que necesitamos, se procede a salir del shell
- Dado que la nuestra lista de elementos en la web utiliza paginación, se añadirá el código correspondiente
    más adelante para poder scrapear las demás páginas 
