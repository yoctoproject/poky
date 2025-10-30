# Bitacora Nagel Mejía Segura

## Día 28 de octubre del 2025

- **`Completado`**: Se siguió una guía para generar una imagen de poky para raspberry pi, se utilizó una layer especifica de raspberrypi. La imagen se quedó cocinando.

- **`Problemas`**: Se trató, de generar el bblayers de forma general para que cualquiera con el repositorio se dedicara simplemente a cocinar la receta, sin embargo, no se logró.

- **`Tareas próximas`**: Probar la imagen minima en la Raspberry Pi, y empezar con la aplicación principal para detectar autos, personas y animales.

- **`Referencias`**: https://www.packtpub.com/de-th/learning/how-to-tutorials/building-our-first-poky-image-raspberry-pi

## Día 29 de octubre del 2025

- **`Completado`**:
  - Se modificó bblayers general para uso compartido.
  - Se probó la imagen generada con Yocto en la Raspberry Pi 5, funcionando correctamente.
  - Se inició una investigación para seleccionar un modelo entrenado para tensorflow lite a utilizar para la detección.

- **`Tareas próximas`**: Es necesario utilizar y generar programas de prueba, para comparar el rendimiento de los modelos.

- **`Referencias`**:
  - https://www.kaggle.com/models/kaggle/yolo-v5
  - https://www.kaggle.com/models/tensorflow/ssd-mobilenet-v1
  - https://www.kaggle.com/models/tensorflow/efficientdet
  - https://www.kaggle.com/models/google/mobile-object-localizer-v1
