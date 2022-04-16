# cliente_servidor_1

 Se desea realizar un programa para obtener periódicamente(Deberás establecer primero una conexión inicial para comprobar su funcionamiento y más tarde una conexión múltiple) datos meteorológicos de un determinado lugar remoto. Los datos que se pueden solicitar son: temperatura mínima, temperatura máxima, presión y pluviometría. Cada uno de estos datos se puede pedir de forma independiente. Para ello se utilizará una comunicación donde

Servidor: Se queda esperando peticiones de conexión. Recibe peticiones de información y devuelve el valor correspondiente. Los valores devueltos son del tipo float. La atención al servicio se realizará utilizando un servidor multihilo.

Cliente: Periódicamente (defina una constante para este periodo) se conecta al servidor meteorológico y solicita por orden la temperatura mínima, temperatura máxima, presión y pluviometría, e imprime todos los valores recibidos por pantalla.

