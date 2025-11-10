#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========================================================
 Proyecto: Deteccion de Trafico en Tiempo Real
 File: traffic_detection.py
 Autores: Nagel Mejía Segura, Wilberth Gutiérrez Montero, Óscar González Cambronero.
 Fecha: 2025-11-09
Descripción:
     Este script implementa un sistema de detección de objetos en tiempo real
     para monitoreo de tráfico utilizando TensorFlow Lite. Detecta vehículos,
     peatones, semáforos y otros objetos relacionados con el tráfico en video
     en vivo o grabado.

 Dependencias de pip:
     - tensorflow
     - opencv-python
     - numpy
     - ai-edge-litert (Opcional, si no está presente hace fallback a tensorflow)

==========================================================
"""

import cv2
import numpy as np
from typing import List, Tuple
import os
import argparse

# Usar TensorFlow Lite interpreter (Compatible con Python 3.13), en caso de no estar disponible, usar TensorFlow.
try:
    from ai_edge_litert.interpreter import Interpreter
except ImportError:
    import tensorflow as tf
    Interpreter = tf.lite.Interpreter


class TrafficObjectDetector:
    """
    Clase para detección de objetos de tráfico usando TensorFlow Lite.
    """

    def __init__(self, model_path: str = None, labels_path: str = None):
        """
        Constructor para inicializar el detector.

        Args:
            model_path: ruta del modelo TFLite
            labels_path: ruta al archivo de etiquetas
        """
        # Si el usuario no proporciona una ruta de modelo, usar la predeterminada
        if model_path is None:
            default_path = os.path.join("modelos", "detect.tflite")
            if not os.path.exists(default_path):
                raise FileNotFoundError(
                    f"\n{'='*60}\n"
                    f"ERROR: ¡Modelo no encontrado!\n"
                    f"{'='*60}\n"
                    f"Ubicación esperada: {default_path}\n\n"
                    f"Asegúrate de que el modelo esté en la ubicación correcta.\n\n"
                    f"O especifica una ruta de modelo personalizada:\n"
                    f"  detector = TrafficObjectDetector(model_path='ruta/al/modelo.tflite')\n"
                    f"{'='*60}\n"
                )
            model_path = default_path
            print(f"Modelo encontrado: {model_path}")

        self.model_path = model_path
        self.labels_path = labels_path or os.path.join(
            "modelos", "labelmap.txt")

        # Cargar etiquetas
        self.labels = self._load_labels()

        # Inicializar intérprete TFLite
        self.interpreter = Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()

        # Obtener detalles de entrada y salida
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # Obtener dimensiones de entrada
        self.input_shape = self.input_details[0]['shape']
        self.height = self.input_shape[1]
        self.width = self.input_shape[2]

        # Especificar clases de tráfico de interés
        self.traffic_classes = {
            0: 'persona',
            1: 'bicicleta',
            2: 'carro',
            3: 'motocicleta',
            5: 'autobús',
            7: 'camión',
            9: 'semáforo',
            11: 'señal de alto',
            12: 'parquímetro'
        }

    def _load_labels(self) -> List[str]:
        """Cargar etiquetas desde archivo."""
        if os.path.exists(self.labels_path):
            with open(self.labels_path, 'r') as f:
                return [line.strip() for line in f.readlines()]
        else:
            return ['person', 'bicycle', 'car', 'motorcycle', 'airplane',
                    'bus', 'train', 'truck', 'boat', 'traffic light',
                    'fire hydrant', 'stop sign', 'parking meter']

    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """Preprocesar el frame para la entrada del modelo."""
        img = cv2.resize(frame, (self.width, self.height))

        # Convertir a RGB si es necesario
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        elif img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Agregar dimensión de lote y convertir a uint8
        input_data = np.expand_dims(img, axis=0).astype(np.uint8)

        return input_data

    def detect_objects(self, frame: np.ndarray,
                       confidence_threshold: float = 0.5) -> List[dict]:
        """
        Detectar objetos en el frame dado.

        Args:
            frame: Frame de video como un array numpy
            confidence_threshold: Connfianza mínima para considerar una detección válida

        Returns:
            Lista de detecciones con formato:
            [
                {'class_id': int,
                 'class_name': str,
                 'confidence': float,
                 'bbox': {'xmin': int, 'ymin': int, 'xmax': int, 'ymax': int}
                },
        """
        input_data = self.preprocess_frame(frame)

        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()

        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        classes = self.interpreter.get_tensor(
            self.output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(
            self.output_details[2]['index'])[0]

        h, w = frame.shape[:2]

        # Filtrar detecciones por umbral de confianza
        detections = []
        for i in range(len(scores)):
            if scores[i] > confidence_threshold:
                class_id = int(classes[i])

                # Centrar solo en clases de tráfico
                if class_id in self.traffic_classes:
                    ymin, xmin, ymax, xmax = boxes[i]

                    detection = {
                        'class_id': class_id,
                        'class_name': self.traffic_classes[class_id],
                        'confidence': float(scores[i]),
                        'bbox': {
                            'xmin': int(xmin * w),
                            'ymin': int(ymin * h),
                            'xmax': int(xmax * w),
                            'ymax': int(ymax * h)
                        }
                    }
                    detections.append(detection)

        return detections

    def draw_detections(self, frame: np.ndarray,
                        detections: List[dict]) -> np.ndarray:
        """Dibujar las detecciones en el frame."""
        output_frame = frame.copy()

        # Mapa de colores para diferentes clases
        colors = {
            'persona': (0, 255, 0),      # Verde
            'carro': (255, 0, 0),        # Azul
            'camión': (255, 100, 0),     # Azul oscuro
            'autobús': (255, 150, 0),    # Azul claro
            'motocicleta': (0, 255, 255),  # Amarillo
            'bicicleta': (0, 200, 255),  # Naranja
            'semáforo': (0, 0, 255),     # Rojo
            'señal de alto': (0, 0, 200),  # Rojo oscuro
        }

        for det in detections:
            bbox = det['bbox']
            class_name = det['class_name']
            confidence = det['confidence']

            # Obtener color
            color = colors.get(class_name, (255, 255, 255))

            # Dibujar caja
            cv2.rectangle(output_frame,
                          (bbox['xmin'], bbox['ymin']),
                          (bbox['xmax'], bbox['ymax']),
                          color, 2)

            # Dibujar etiqueta
            label = f"{class_name}: {confidence:.2f}"
            label_size, _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)

            cv2.rectangle(output_frame,
                          (bbox['xmin'], bbox['ymin'] - label_size[1] - 10),
                          (bbox['xmin'] + label_size[0], bbox['ymin']),
                          color, -1)

            cv2.putText(output_frame, label,
                        (bbox['xmin'], bbox['ymin'] - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        return output_frame

    def process_video(self, video_source: str = 0,
                      output_path: str = None,
                      show_window: bool = True,
                      confidence_threshold: float = 0.5):
        """
        Procesar video para detección de objetos.

        Args:
            video_source: Ruta del archivo de video o índice del dispositivo de cámara
            output_path: Ruta del archivo de video de salida (opcional)
            show_window: Booleano para mostrar ventana de video
            confidence_threshold: Umbral de confianza para detecciones
        """
        # Abrir fuente de video
        cap = cv2.VideoCapture(video_source)

        if not cap.isOpened():
            raise ValueError(
                f"No se pudo abrir recurso de video: {video_source}")

        # Obtener propiedades del video
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        if fps == 0:
            fps = 30
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(f"Propiedades del video: {width}x{height} @ {fps} fps")

        # Configurar escritor de video si se proporciona una ruta de salida
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            print(f"Grabando en: {output_path}")

        # Crear ventana si es necesario
        if show_window:
            cv2.namedWindow('Detector de Tráfico', cv2.WINDOW_NORMAL)

        print("Iniciando detección... Presiona 'q' para salir")

        frame_count = 0
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Detectar objetos
                detections = self.detect_objects(frame, confidence_threshold)

                # Dibujar detecciones
                output_frame = self.draw_detections(frame, detections)

                # Añadir estadísticas
                stats_text = f"Cuadro: {frame_count} | Objetos: {len(detections)}"
                cv2.putText(output_frame, stats_text, (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Escribir cuadro en archivo de salida
                if writer:
                    writer.write(output_frame)

                # Mostrar ventana
                if show_window:
                    cv2.imshow('Detector de Tráfico', output_frame)

                    # Esperar tecla 'q' para salir
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                frame_count += 1

                # Estadísticas cada 30 cuadros
                if frame_count % 30 == 0:
                    print(f"Procesados {frame_count} cuadros...", end='\r')

        finally:
            cap.release()
            if writer:
                writer.release()
            if show_window:
                cv2.destroyAllWindows()

            print(f"\nProcesados {frame_count} cuadros en total")


# Ejecución principal
if __name__ == "__main__":
    # Extraer argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description='Detección de Objetos de Tráfico usando TensorFlow Lite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Usar dispositivo de cámara USB
  python script.py --d /dev/video0
  
  # Procesar archivo de video (por defecto)
  python script.py video_trafico.mp4
  
  # Procesar video y guardar salida
  python script.py video_trafico.mp4 --output salida_detectada.mp4
        """
    )

    parser.add_argument(
        'input',
        nargs='?',
        default=None,
        help='Archivo de video de entrada (.mp4). No necesario si se usa --d para dispositivo de cámara.'
    )

    parser.add_argument(
        '--d',
        dest='device',
        type=str,
        default=None,
        help='Archivo de dispositivo de cámara USB (ej., /dev/video0, /dev/video1)'
    )

    parser.add_argument(
        '--output',
        '-o',
        type=str,
        default=None,
        help='Ruta del archivo de video de salida (opcional)'
    )

    parser.add_argument(
        '--confidence',
        '-c',
        type=float,
        default=0.5,
        help='Umbral de confianza para detecciones (por defecto: 0.5)'
    )

    parser.add_argument(
        '--no-display',
        action='store_true',
        help='No mostrar ventana de video (útil para sistemas sin interfaz gráfica)'
    )

    args = parser.parse_args()

    # Validar entradas
    if args.device is None and args.input is None:
        parser.error(
            "Debe proporcionar un archivo de video o usar --d para especificar un dispositivo de cámara")

    if args.device and args.input:
        parser.error(
            "No se puede usar ambos --d (dispositivo de cámara) y archivo de video simultáneamente")

    # Determinar fuente de video
    if args.device:
        print(f"Usando dispositivo de cámara: {args.device}")
        video_source = args.device
    else:
        if not os.path.exists(args.input):
            print(f"Error: Archivo de video no encontrado: {args.input}")
            exit(1)
        print(f"Usando archivo de video: {args.input}")
        video_source = args.input

    # Inicializar detector
    print("\nInicializando detector de objetos...")
    try:
        detector = TrafficObjectDetector()
    except FileNotFoundError as e:
        print(e)
        exit(1)

    # Procesar video
    print(f"\nIniciando detección (umbral de confianza: {args.confidence})...")
    print("Presiona 'q' para salir\n")

    try:
        detector.process_video(
            video_source=video_source,
            output_path=args.output,
            show_window=not args.no_display,
            confidence_threshold=args.confidence
        )
    except KeyboardInterrupt:
        print("\n\nInterrumpido por el usuario")
    except Exception as e:
        print(f"\nError durante el procesamiento: {e}")
        exit(1)

    print("\nFin de la ejecución.")
