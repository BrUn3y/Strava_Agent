# 🎯 Ejemplos de Prompts - Aprovecha Todo el Potencial del Agente

Esta guía contiene ejemplos de prompts diseñados para aprovechar al máximo las capacidades de tu Strava Agent con Think Tool y Python Tool.

## 📊 Nivel 1: Consultas Básicas (Solo Strava Tools)

### Actividades Recientes
```
"Muéstrame mis últimas 10 actividades en una tabla"
```
**Resultado esperado:** Tabla con fecha, tipo, distancia, tiempo, ritmo

```
"Dame detalles completos de mi última carrera"
```
**Resultado esperado:** Información detallada con mapa de ruta

```
"¿Cuáles fueron mis actividades de la semana pasada?"
```
**Resultado esperado:** Tabla filtrada por fecha

### Estadísticas
```
"Muestra mis estadísticas totales de running"
```
**Resultado esperado:** Tabla con distancia total, tiempo, elevación

```
"¿Cuántos kilómetros he corrido este año?"
```
**Resultado esperado:** Resumen con estadísticas del año

## 🧠 Nivel 2: Análisis con Think Tool

### Comparaciones Inteligentes
```
"Compara mis últimas 5 carreras y dime si estoy mejorando mi ritmo"
```
**Herramientas usadas:** Think + GetActivities
**Resultado esperado:** 
- Tabla comparativa de las 5 carreras
- Análisis de tendencia de ritmo
- Conclusión sobre mejora

```
"Analiza mi consistencia de entrenamiento en las últimas 4 semanas"
```
**Herramientas usadas:** Think + GetActivities
**Resultado esperado:**
- Tabla de actividades por semana
- Análisis de frecuencia
- Recomendaciones

### Análisis de Patrones
```
"¿Qué patrones ves en mis entrenamientos? ¿Entreno más entre semana o fines de semana?"
```
**Herramientas usadas:** Think + GetActivities
**Resultado esperado:**
- Tabla agrupada por día de semana
- Análisis de patrones
- Insights sobre hábitos

```
"Compara mi rendimiento en carreras matutinas vs vespertinas"
```
**Herramientas usadas:** Think + GetActivities
**Resultado esperado:**
- Tabla comparativa por horario
- Análisis de diferencias
- Recomendación de mejor horario

## 🐍 Nivel 3: Análisis Avanzado con Python Tool

### Visualizaciones de Tendencias
```
"Crea una gráfica mostrando la evolución de mi ritmo en los últimos 30 días"
```
**Herramientas usadas:** Think + GetActivities + Python
**Resultado esperado:**
- Tabla de datos
- Gráfica de línea con tendencia
- Análisis estadístico (mejora promedio, desviación)

```
"Genera un gráfico de barras con mi kilometraje semanal del último mes"
```
**Herramientas usadas:** Think + GetActivities + Python
**Resultado esperado:**
- Tabla de km por semana
- Gráfico de barras
- Comparación semana a semana

### Análisis Estadístico
```
"Calcula la correlación entre mi distancia y frecuencia cardíaca promedio"
```
**Herramientas usadas:** Think + GetActivities + Python
**Resultado esperado:**
- Tabla de datos
- Coeficiente de correlación
- Gráfico de dispersión
- Interpretación del resultado

```
"Muéstrame un histograma de la distribución de mis zonas de frecuencia cardíaca"
```
**Herramientas usadas:** Think + GetActivities + GetActivityZones + Python
**Resultado esperado:**
- Tabla de tiempo por zona
- Histograma visual
- Análisis de distribución

### Comparaciones Complejas
```
"Compara estadísticamente mis carreras de 10km vs 5km: ritmo, FC, y cadencia"
```
**Herramientas usadas:** Think + GetActivities + Python
**Resultado esperado:**
- Tabla comparativa con promedios
- Gráficos de caja (box plots)
- Análisis estadístico (media, mediana, desviación)
- Conclusiones

```
"Analiza cómo varía mi rendimiento según el día de la semana con gráficos"
```
**Herramientas usadas:** Think + GetActivities + Python
**Resultado esperado:**
- Tabla por día de semana
- Gráfico de barras o líneas
- Análisis de variabilidad
- Mejor día para entrenar

## 🎯 Nivel 4: Análisis Multidimensional

### Análisis de Progreso
```
"Analiza mi progreso en los últimos 3 meses: crea tablas y gráficos mostrando evolución de distancia, ritmo y frecuencia cardíaca"
```
**Herramientas usadas:** Think + GetActivities + GetAthleteStats + Python
**Resultado esperado:**
- Tabla mensual de métricas
- 3 gráficos de tendencia
- Análisis de mejora porcentual
- Proyección futura

### Análisis de Zonas de Entrenamiento
```
"Muestra en qué zonas de FC he entrenado más este mes y crea una visualización"
```
**Herramientas usadas:** Think + GetActivities + GetActivityZones + Python
**Resultado esperado:**
- Tabla de tiempo por zona
- Gráfico de pastel o barras
- Análisis de distribución
- Recomendaciones de balance

### Análisis de Eficiencia
```
"Calcula mi eficiencia de entrenamiento: relación entre distancia, tiempo y frecuencia cardíaca en las últimas 20 carreras"
```
**Herramientas usadas:** Think + GetActivities + Python
**Resultado esperado:**
- Tabla de métricas de eficiencia
- Gráficos de correlación
- Score de eficiencia
- Tendencia de mejora

### Comparación de Segmentos
```
"Compara mi rendimiento en diferentes segmentos: encuentra patrones en mis mejores tiempos"
```
**Herramientas usadas:** Think + GetActivities + GetActivityStreams + Python
**Resultado esperado:**
- Tabla de segmentos y tiempos
- Análisis de factores comunes
- Gráficos comparativos
- Recomendaciones

## 🏆 Nivel 5: Análisis Predictivo y Avanzado

### Predicciones
```
"Basándote en mi progreso de los últimos 2 meses, predice cuándo podré correr 10km en menos de 45 minutos"
```
**Herramientas usadas:** Think + GetActivities + Python (regresión lineal)
**Resultado esperado:**
- Tabla de progreso histórico
- Gráfico con línea de tendencia
- Predicción con fecha estimada
- Confianza de la predicción

### Análisis de Recuperación
```
"Analiza el tiempo entre mis entrenamientos y cómo afecta mi rendimiento"
```
**Herramientas usadas:** Think + GetActivities + Python
**Resultado esperado:**
- Tabla de días de descanso vs rendimiento
- Gráfico de correlación
- Análisis estadístico
- Recomendación de días óptimos de descanso

### Análisis de Carga de Entrenamiento
```
"Calcula mi carga de entrenamiento semanal y muestra si estoy en riesgo de sobreentrenamiento"
```
**Herramientas usadas:** Think + GetActivities + Python
**Resultado esperado:**
- Tabla de carga por semana
- Gráfico de tendencia de carga
- Ratio agudo:crónico
- Alertas y recomendaciones

### Optimización de Entrenamiento
```
"Analiza todos mis datos y recomienda el mejor plan de entrenamiento para mejorar mi medio maratón"
```
**Herramientas usadas:** Think + GetActivities + GetAthleteStats + Python
**Resultado esperado:**
- Análisis completo de estado actual
- Identificación de debilidades
- Plan de entrenamiento personalizado
- Gráficos de progreso esperado

## 💡 Tips para Mejores Prompts

### ✅ Prompts Efectivos:
1. **Sé específico con el período de tiempo**
   - ❌ "Muestra mis carreras"
   - ✅ "Muestra mis carreras de las últimas 2 semanas"

2. **Pide visualizaciones explícitamente**
   - ❌ "Analiza mi progreso"
   - ✅ "Analiza mi progreso con gráficos y tablas"

3. **Combina múltiples métricas**
   - ❌ "¿Cómo está mi ritmo?"
   - ✅ "Compara mi ritmo, FC y cadencia en las últimas 10 carreras"

4. **Pide análisis, no solo datos**
   - ❌ "Dame mis estadísticas"
   - ✅ "Analiza mis estadísticas y dime qué debo mejorar"

### 🎯 Estructura de Prompt Ideal:
```
[Acción] + [Datos específicos] + [Período] + [Formato deseado] + [Análisis]

Ejemplo:
"Compara [acción] mis últimas 15 carreras [datos] del último mes [período] 
en una tabla y gráfico [formato] y dime si estoy mejorando [análisis]"
```

## 🔥 Prompts Avanzados para Casos Específicos

### Para Preparar una Carrera
```
"Analiza mis últimos 3 meses de entrenamiento y dime si estoy listo para un medio maratón. 
Muestra tablas de progreso, gráficos de tendencia y dame recomendaciones específicas."
```

### Para Identificar Problemas
```
"Compara mis carreras de este mes con el mes pasado. Identifica cualquier disminución 
en rendimiento y sugiere posibles causas con datos y gráficos."
```

### Para Optimizar Zonas
```
"Analiza en qué zonas de FC he entrenado en los últimos 30 días, crea visualizaciones 
y recomienda cómo balancear mejor mi entrenamiento."
```

### Para Tracking de Objetivos
```
"Mi objetivo es correr 200km este mes. Muestra mi progreso actual en tabla y gráfico, 
calcula cuánto debo correr por semana para lograrlo."
```

## 📈 Ejemplos de Salidas Esperadas

### Ejemplo 1: Análisis de Progreso
**Prompt:** "Analiza mi progreso de ritmo en las últimas 10 carreras con gráfico"

**Salida esperada:**
```
## 📊 Análisis de Progreso de Ritmo

| Fecha | Distancia (km) | Tiempo (min) | Ritmo (min/km) |
|-------|---------------|--------------|----------------|
| 2025-01-20 | 10.5 | 52 | 4:57 |
| 2025-01-18 | 8.2 | 38 | 4:38 |
| ... | ... | ... | ... |

[Gráfico de línea mostrando tendencia]

### Análisis:
- Mejora promedio: -8 segundos/km por semana
- Mejor ritmo: 4:38 min/km (2025-01-18)
- Tendencia: Positiva ✅
- Proyección: Podrías alcanzar 4:30 min/km en 2 semanas
```

### Ejemplo 2: Comparación Estadística
**Prompt:** "Compara estadísticamente mis carreras de 5km vs 10km"

**Salida esperada:**
```
## 📊 Comparación 5km vs 10km

| Métrica | 5km | 10km | Diferencia |
|---------|-----|------|------------|
| Ritmo promedio | 4:35 | 4:52 | +17 seg/km |
| FC promedio | 165 bpm | 158 bpm | -7 bpm |
| Cadencia | 178 spm | 175 spm | -3 spm |

[Gráficos de caja comparativos]

### Conclusiones:
- Mantienes mejor ritmo en distancias cortas
- FC más controlada en distancias largas
- Cadencia consistente en ambas distancias
```

## 🎓 Aprende Más

- Para configurar Python Tool: Ver [ADVANCED_TOOLS_GUIDE.md](ADVANCED_TOOLS_GUIDE.md)
- Para troubleshooting: Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Para documentación completa: Ver [README.md](README.md)

---

**¡Experimenta con estos prompts y descubre insights sobre tu entrenamiento! 🏃‍♂️📊**