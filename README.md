# StrengthXP

Este proyecto analiza el rendimiento físico y la progresión de fuerza a partir de registros diarios de entrenamiento. Su objetivo principal es eliminar el entrenamiento "a ciegas", permitiendo tomar decisiones basadas en datos para optimizar el rendimiento, verificar la progresión y asegurar un adecuado equilibrio muscular.

[DashBoard](https://datastudio.google.com/u/0/reporting/09ee3103-5149-4e5f-be19-edf85b062a61/page/lsx8F)

---

##  ¿Qué analiza el proyecto?

* **Volumen de Carga Total:** Mide el trabajo total acumulado por sesión, ejercicio y grupo muscular para evaluar el estímulo de hipertrofia.
* **Estimación de Fuerza Máxima (1RM):** Utiliza la fórmula de Epley para calcular el rendimiento máximo teórico a una repetición sin exponer el cuerpo a cargas de alto riesgo.
* **Sobrecarga Progresiva:** Rastrea la evolución temporal de pesos y repeticiones por ejercicio para verificar la progresión sesión a sesión.
* **Balance por Grupo Muscular:** Visualiza la distribución del volumen de trabajo semanal (Pecho, Espalda, Piernas, etc.) para prevenir descompensaciones en la rutina.
* **Record Personal (PR):** Registra el peso máximo alcanzado por ejercicio, junto al 1RM con su respectiva fecha para poder medir la fuerza histórica.

---

##  Arquitectura del Pipeline

El pipeline de datos sigue el siguiente flujo de procesamiento:

1. **Extracción y Limpieza:** Lectura dinámica desde **Google Sheets** utilizando **Python** y **`pandas`** para la desduplicación, manejo de valores nulos y parseo de fechas.
2. **Transformación (KPIs):** Categorización automática de músculos principales/secundarios mediante mapeos dict y cálculo iterativo de 1RM, tonelaje por serie y desglose semanal con **`numpy`**.
3. **Carga (ETL):** Exportación automatizada de DataFrames procesados hacia múltiples pestañas del Spreadsheet mediante las APIs de **`gspread`** y **`gspread-dataframe`**.
4. **Visualización:** Consumo del modelo de datos unificado en **Looker Studio** para la generación de un dashboard interactivo.

---
## Dashboard
<img width="1118" height="825" alt="1" src="https://github.com/user-attachments/assets/6eac8031-e4da-4ff5-9f1e-4abee866fd4e" />
<img width="1112" height="793" alt="2" src="https://github.com/user-attachments/assets/fc526b03-1f63-4a2c-93e1-50c6423f458a" />

---
## 🚨 Importante 🚨:
Toda la información y métricas mostradas tienen fines estrictamente demostrativos e informativos. No constituyen asesoramiento médico ni entrenamiento 
profesional. Consulta con un profesional de la salud o del deporte calificado antes de iniciar o modificar cualquier programa de entrenamiento.

---
## ¿Cómo interpretar los datos?
### Estimación de fuerza 1RM:
El 1RM no indica una estimación del peso máximo que podemos levantar en 1 repetición. Con esta información, el gráfico nos brinda la posibilidad de aumentar dicho peso progresivamente y sin lesiones; es decir.
### Balance por grupo muscular:
El gráfico de tortas nos proporciona un porcentaje visual muy fácil de interpretar y saber qué músculos son los que más entrenamos y cuáles son los que menos.
Con esta información podemos ajustar nuestra rutina para poder tener un entrenamiento equilibrado y evitar una descompensación muscular.
### Hipertrofia:
Por cada semana se evalúa la cantidad de series y el tonelaje total en la semana; gracias a esta información, podemos ayudarnos de la siguiente información.
* Cantidad de series igual o sutilmente similar por semana + aumento de peso = resultados excelentes para la hipertrofia.
* Cantidad de series mayor + aumento de peso = resultados buenos para la hipertrofia; se recomienda monitorear la recuperación para no fatigarse.
* Cantidad de series mayor o igual + disminución del peso = malo para la hipertrofia, se recomienda subir el peso y bajar las repeticiones.
### Sobrecarga Progresiva:
Con la información obtenida con el gráfico de hipertrofia podemos ir gradualmente aumentando el peso para generar sobrecarga progresiva. Dicha información será volcada en este gráfico mostrando peso y repeticiones entre semanas, para poder ir graduando nuestros pesos y evitar la fatiga.
* Si la caída es planificada, corresponde a una semana de descarga (deload) para disipar fatiga.
* Si NO es planificada: Indica acumulación de fatiga excesiva o falta de rendimiento, lo que justifica ajustar la programación.
### Tabla historial y PR Global:
En la tabla podemos comparar los récords personales de cada ejercicio para ponernos nuevas metas y poder aumentar nuestra carga progresivamente con la ayuda de la columna de 1RM para no generar fatiga y no exceder el peso.

---
##  Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Librerías:** `pandas`, `numpy`, `gspread`, `gspread-dataframe`
* **Almacenamiento y Plataforma:** Google Cloud Platform (APIs de Sheets y Drive)
* **Visualización de Datos:** Looker Studio
