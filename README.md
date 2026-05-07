# Senderos del Zipa - Sistema de Seguridad Vehicular (Prototipo TRL5)

## Descripcion del Proyecto
Este repositorio contiene el desarrollo ingenieril del sistema "Senderos del Zipa", un prototipo funcional diseñado para la automatizacion del control de acceso vehicular en conjuntos residenciales. El sistema integra Vision Artificial y conectividad en la nube para fortalecer la seguridad perimetral mediante la identificacion automatica de placas.

Este desarrollo corresponde a la Fase 4 (Componente Practico) del curso Proyecto de Grado de la UNAD.

## Arquitectura Tecnica (Edge-Cloud)
El sistema opera bajo un modelo de computacion distribuida:
- Capa Edge: Procesamiento local en Python mediante la libreria OpenCV y el motor de OCR Tesseract para el reconocimiento de placas en tiempo real.
- Capa Cloud: Integracion con la API de Telegram para el envio de alertas instantaneas y registros de acceso a dispositivos moviles de forma remota.

## Funcionalidades Principales
-受 Reconocimiento de Placas: Procesamiento de caracteres alfanumericos mediante filtros de umbralizacion y procesamiento digital de imagenes.
- Validacion de Residentes: Contraste inmediato de la placa detectada con una base de datos local (residentes.txt).
- Pausa de Confirmacion: El sistema realiza una detencion logica de 3 segundos al detectar una coincidencia para garantizar la trazabilidad visual y el envio de datos.
- Alertas en Tiempo Real: Notificaciones diferenciadas (Acceso Autorizado / Alerta de Sospechoso) enviadas a traves de un bot de Telegram.

## Requisitos de Instalacion
Para ejecutar el prototipo en un entorno local, se requiere:
1. Python 3.10 o superior.
2. Tesseract OCR instalado en el sistema (ruta por defecto: C:\Program Files\Tesseract-OCR).
3. Instalacion de dependencias mediante el comando:
   pip install opencv-python pytesseract pillow requests numpy

## Instrucciones de Uso
1. Configurar la direccion IP de la fuente de video (IP Webcam) en el script principal.
2. Validar que las credenciales de la API de Telegram (Token y Chat ID) sean correctas.
3. Ejecutar el script principal:
   python codigo2.py

## Informacion Academica
- Institucion: Universidad Nacional Abierta y a Distancia (UNAD)
- Curso: Proyecto de Grado
- Fase: 4 - Desarrollo de la propuesta ingenieril
- Nivel de Madurez Tecnologica: TRL5 (Prototipo validado en entorno relevante)
- Autor: EdWIN Fernando Ochoa Arenas

---
Este proyecto se entrega como evidencia del componente practico y cumplimiento de la metodologia ingenieril propuesta en el documento maestro.
