# **Gestión eficiente de recursos en sistemas ferroviarios**

## Descripción
Con este programa buscamos abordar la planificación eficiente de la circulación de material rodante en sistemas ferroviarios para reducir costos y mejorar la sostenibilidad. Modelamos la red ferroviaria como un digrafo, donde cada evento de llegada y partida de tren se representa como un vértice. Utilizamo un algoritmo de flujo de costo mínimo para calcular la cantidad óptima de vagones necesarios, minimizando el uso de recursos. 

## Requisitos

- Python 3.x
- Networkx


## Instancias de Prueba
Dentro de instances se encuentran las siguientes instancias de prueba que corresponden a distintos cronogramas ferroviarios:
- toy_instance.json
- retiro-tigre-semana.json
- maipu-delta-semana.json
- maipu-delta-semana-HP.jspon
- maipu-delta-finde.json

## Uso

1. Clona este repositorio o descarga los archivos del mismo.
2. Asegúrate de tener las dependencias instaladas.
3. Selecciona la instancia que quieras probrar, descomentando la misma del código.
4. Cambia el valor de flag de la siguiente manera, según tus necesidades:
    - flag = False: Permitir un número ilimitado de unidades durante la noche.
    - flag = True: Activar la limitación en la cantidad de unidades que pueden permanecer durante la noche en una estación. En este caso, se deberá establecer dicha limitación dentro del json utilizado, en el valor "night_capacity". Por defecto, cada instancia tendrá como night_capacity la cantidad de unidades que permanecen en cada estación del flujo original.

## Resultados
Una vez completada la ejecución, se imprimirán por pantalla un diccionario con el flujo de costo mínimo de la instancia utilizada y dos strings con la cantidad de vagones que permanecen en cada estación.
