# Sistema Automatizado de Horarios CAMCM

## Descripción

Este sistema permite generar de forma automatizada los horarios académicos del Centro de Actualización del Magisterio en la Ciudad de México (CAMCM), considerando las restricciones institucionales y validando posibles conflictos mediante técnicas de aprendizaje automático (Random Forest).

El sistema ofrece una interfaz gráfica sencilla para usuarios administrativos, permitiendo generar, validar y exportar horarios de forma eficiente.

---

## Estructura del Proyecto

```
CAMCM_Horarios/
├── modelo.py           # Entrenamiento del modelo Random Forest
├── generador.py        # Generación automática de horarios
├── validacion.py       # Validación de traslapes y conflictos
├── exportador.py       # Exportación de horarios a CSV
├── interfaz.py         # Interfaz gráfica para usuarios
├── config.json         # Configuración institucional (editable)
├── README.md           # Documentación del proyecto
├── requirements.txt    # Librerías necesarias
└── horario_validado.csv # Resultado exportado
```

---

## Instalación

1. Instalar Python 3.11.7 o superior.
2. Instalar las dependencias:

```
pip install -r requirements.txt
```

---

## Uso

### Desde interfaz gráfica

Ejecutar:

```
python interfaz.py
```

### Funciones disponibles:

- **Generar Horario** → Genera automáticamente el horario considerando restricciones.
- **Validar Traslapes** → Verifica conflictos en el horario generado.
- **Exportar Horario** → Exporta el horario en formato CSV compatible con Excel.

### Generar ejecutable (.exe) (opcional)

```
pip install pyinstaller
pyinstaller --onefile --windowed interfaz.py
```

El ejecutable quedará en `/dist/interfaz.exe`.

---

## Autor

Julio César Santa Rita Ávila  
Maestría en Informática - Instituto Politécnico Nacional (IPN)  
Sistema desarrollado para el CAMCM - Proyecto de tesis 2025

---

## Licencia

Uso interno educativo.