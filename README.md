# StrengthXP

Este proyecto analiza el rendimiento físico y la progresión de fuerza a partir de registros diarios de entrenamiento. Su objetivo principal es eliminar el entrenamiento "a ciegas", permitiendo tomar decisiones basadas en datos para optimizar el rendimiento, verificar la progresión y asegurar un adecuado equilibrio muscular.

---

##  ¿Qué analiza el proyecto?

* **Volumen de Carga Total:** Mide el trabajo total acumulado por sesión, ejercicio y grupo muscular para evaluar el estímulo de hipertrofia.
* **Estimación de Fuerza Máxima (1RM):** Utiliza la fórmula de Epley para calcular el rendimiento máximo teórico a una repetición sin exponer el cuerpo a cargas de alto riesgo.
* **Sobrecarga Progresiva:** Rastrea la evolución temporal de pesos y repeticiones por ejercicio para verificar la progresión sesión a sesión.
* **Balance por Grupo Muscular:** Visualiza la distribución del volumen de trabajo semanal (Pecho, Espalda, Piernas, etc.) para prevenir descompensaciones en la rutina.
* **Record Personal (PR):** Registra el peso máximo alcanzado por ejercicio, junto al 1RM con su respectiva fecha para poder medir la fuerza histórica

---

##  Arquitectura del Pipeline

El pipeline de datos sigue el siguiente flujo de procesamiento:

1. **Extracción y Limpieza:** Lectura dinámica desde **Google Sheets** utilizando **Python** y **`pandas`** para la desduplicación, manejo de valores nulos y parseo de fechas.
2. **Transformación (KPIs):** Categorización automática de músculos principales/secundarios mediante mapeos dict y cálculo iterativo de 1RM, tonelaje por serie y desglose semanal con **`numpy`**.
3. **Carga (ETL):** Exportación automatizada de DataFrames procesados hacia múltiples pestañas del Spreadsheet mediante la API de **`gspread`** y **`gspread-dataframe`**.
4. **Visualización:** Consumo del modelo de datos unificado en **Looker Studio** para la generación de un dashboard interactivo.

---

##  Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Librerías:** `pandas`, `numpy`, `gspread`, `gspread-dataframe`
* **Almacenamiento y Plataforma:** Google Cloud Platform (APIs de Sheets y Drive)
* **Visualización de Datos:** Looker Studio
