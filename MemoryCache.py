# Importar las bibliotecas necesarias
import heapq
from collections import deque, defaultdict

# Definir la clase CacheSimulator que simula una caché
class CacheSimulator:
    def __init__(self, capacity, eviction_policy='LRU'):
        # Inicializar la caché con una capacidad dada y una política de reemplazo (LRU por defecto)
        self.capacity = capacity
        self.cache = {}  # Un diccionario para almacenar los elementos de la caché
        self.access_count = {}  # Un diccionario para llevar un registro de las frecuencias de acceso a las claves
        self.eviction_policy = eviction_policy

    def put(self, key, value):
        # Método para insertar un elemento en la caché
        if key in self.cache:  # Si la clave ya existe en la caché
            self.cache[key] = value  # Actualizar el valor asociado a la clave
            self._update_priority(key)  # Actualizar la prioridad según la política de reemplazo
        else:  # Si la clave no existe en la caché entonces:
            if len(self.cache) >= self.capacity:  # Si la caché está llena
                self._evict()  # Realizar un reemplazo según la política de reemplazo
            self.cache[key] = value  # Insertar el nuevo elemento en la caché
            self.access_count[key] = 1  # Inicializar la frecuencia de acceso a 1

    def get(self, key):
        # Método para recuperar un elemento de la caché
        if key in self.cache:  # Si la clave existe en la caché
            self._update_priority(key)  # Actualizar la prioridad según la política de reemplazo
            return self.cache[key]  # Devolver el valor asociado a la clave
        else:  # Si la clave no existe en la caché
            return None  # Devolver None
                           
    def _update_priority(self, key):
        # Método privado para actualizar la prioridad de una clave según la política LFU
        if self.eviction_policy == 'LFU':
            self.access_count[key] += 1  # Incrementar la frecuencia de acceso a la clave

    def _evict(self):
        # Método privado para realizar un reemplazo en la caché cuando está llena
        if self.eviction_policy == 'LRU':  # Si la política de reemplazo es LRU
            oldest_key = min(self.access_count, key=self.access_count.get)  # Encontrar la clave menos recientemente usada
            del self.cache[oldest_key]  # Eliminar la clave de la caché
            del self.access_count[oldest_key]  # Eliminar la entrada de frecuencia de acceso
        elif self.eviction_policy == 'LFU':  # Si la política de reemplazo es LFU
            min_key = min(self.access_count, key=self.access_count.get)  # Encontrar la clave menos frecuentemente usada
            del self.cache[min_key]  # Eliminar la clave de la caché
            del self.access_count[min_key]  # Eliminar la entrada de frecuencia de acceso

    def change_eviction_policy(self, eviction_policy):
        # Método para cambiar la política de reemplazo de la caché
        self.eviction_policy = eviction_policy  # Actualizar la política de reemplazo
        if eviction_policy == 'LFU':  # Si la nueva política es LFU
            self.access_count = defaultdict(int, self.access_count)  # Reinicializar el contador de frecuencia de acceso
