## [v0.1.2] - 2026-01-22 - Fix LinePrefixParserError

### 🐛 Bug Fixes

**Problema:** Error `LinePrefixParserError: Transition from 'thought' to 'tool_input' does not exist`

Este error ocurría porque el modelo LLM `openai/gpt-oss-120b` no seguía correctamente el formato ReAct requerido por el framework BeeAI.

### ✅ Soluciones Implementadas

1. **Cambio de Modelo LLM por Defecto**
   - Antes: `openai/gpt-oss-120b` (problemas de adherencia al formato)
   - Después: `meta-llama/llama-3-1-70b-instruct` (mejor seguimiento del formato ReAct)

2. **Parámetros LLM Optimizados**
   ```python
   ChatModelParameters(
       temperature=0.0,  # Más determinístico
       max_tokens=2048,
       top_p=0.95,
       top_k=50
   )
   ```

3. **Mejor Manejo de Errores**
   - Mensajes de error más descriptivos
   - Sugerencias automáticas cuando ocurre LinePrefixParserError
   - Guía al usuario sobre cómo resolver el problema

4. **Documentación Completa**
   - Nuevo archivo `TROUBLESHOOTING.md` con guía detallada
   - README actualizado con sección de troubleshooting
   - Modelos LLM recomendados documentados

### 📚 Archivos Modificados

- `src/beeai_agents/agent.py`: Cambio de modelo y parámetros optimizados
- `README.md`: Sección de troubleshooting actualizada
- `TROUBLESHOOTING.md`: Nueva guía completa de solución de problemas

### 🎯 Modelos Recomendados

| Modelo | Estado | Uso |
|--------|--------|-----|
| `meta-llama/llama-3-1-70b-instruct` | ✅ Recomendado | Mejor adherencia al formato ReAct |
| `meta-llama/llama-3-1-8b-instruct` | ✅ OK | Más rápido, menos confiable |
| `ibm/granite-3-8b-instruct` | ✅ OK | Alternativa válida |
| `openai/gpt-oss-120b` | ❌ No recomendado | Problemas de formato |

### 💡 Recomendaciones de Uso

Para evitar errores de formato:
1. Usa el modelo por defecto (llama-3-1-70b-instruct)
2. Simplifica tus consultas
3. Sé más específico en las preguntas
4. Consulta `TROUBLESHOOTING.md` si tienes problemas

---

# Changelog - Actualización BeeAI Framework

## Fecha: 2026-01-22

## Resumen

Se ha actualizado el agente de Strava de una versión deprecada de BeeAI Framework a la versión más reciente (>=0.1.68) basándose en la documentación oficial del repositorio [i-am-bee/beeai-framework](https://github.com/i-am-bee/beeai-framework).

---

## ✅ Cambios Implementados

### 1. **Imports Actualizados**

#### Antes:
```python
from beeai_framework.agents.bee.agent import BeeAgent
from beeai_framework.adapters.watsonx.backend import WatsonxChatModel
```

#### Después:
```python
from beeai_framework.agents.react import ReActAgent
from beeai_framework.adapters.watsonx import WatsonxChatModel
import yaml  # Nuevo import necesario
```

**Razón:** 
- `BeeAgent` ya no existe en la nueva API
- El path de `WatsonxChatModel` cambió de `.backend` a directamente desde `.watsonx`
- Se agregó `yaml` para parsear correctamente el schema de OpenAPI

---

### 2. **Configuración de OpenAPITool**

#### Antes:
```python
strava_tool = OpenAPITool(
    name="StravaReader",
    spec=open("strava-tool.yaml").read(),
    execution_options={
        "headers": lambda: {"Authorization": f"Bearer {auth.get_token()}"}
    }
)
```

#### Después:
```python
with open("strava-tool.yaml") as file:
    strava_schema = yaml.safe_load(file)

strava_tools = OpenAPITool.from_schema(strava_schema)
```

**Razón:**
- La nueva API usa `from_schema()` que espera un diccionario (no string)
- `from_schema()` retorna una lista de herramientas (una por cada operación en el schema)
- El parámetro `name` y `spec` ya no existen en la nueva API

---

### 3. **Inicialización del Agente**

#### Antes:
```python
agent = BeeAgent(
    llm=llm,
    memory=UnconstrainedMemory(),
    tools=[strava_tool]
)
```

#### Después:
```python
agent = ReActAgent(
    llm=llm,
    memory=UnconstrainedMemory(),
    tools=strava_tools
)
```

**Razón:**
- `BeeAgent` fue reemplazado por `ReActAgent` (Reasoning + Acting)
- `ReActAgent` es mejor para análisis complejos y toma de decisiones

---

### 4. **Ejecución del Agente**

#### Antes:
```python
response = await agent.run(prompt=user_query)
print(response.result.text)
```

#### Después:
```python
response = await agent.run(user_query)
try:
    print(response.last_message.text)
except AttributeError:
    print(response)
```

**Razón:**
- El parámetro `prompt` ya no es necesario (se pasa directamente)
- La estructura de respuesta cambió de `response.result.text` a `response.last_message.text`
- Se agregó manejo de errores por si la estructura es diferente

---

## ⚠️ Problemas Conocidos y TODOs

### 1. **Autenticación Dinámica de Strava**

**Estado:** ⚠️ PENDIENTE

La funcionalidad de inyectar headers dinámicos para autenticación OAuth de Strava aún no está implementada en la nueva versión.

**Código Original (Deprecado):**
```python
execution_options={
    "headers": lambda: {"Authorization": f"Bearer {auth.get_token()}"}
}
```

**Soluciones Posibles:**
1. Investigar si `OpenAPITool` tiene un parámetro para configurar headers dinámicos
2. Configurar headers en cada herramienta individualmente después de crearlas
3. Usar middleware o interceptors si están disponibles
4. Verificar documentación para parámetros como `request_options` o similar

**Impacto:** Sin esto, las llamadas a la API de Strava fallarán por falta de autenticación.

---

### 2. **Warnings de Tipo (Type Hints)**

Hay algunos warnings de tipo que no afectan la funcionalidad pero deberían revisarse:

```
- WatsonxChatModel parameters: dict vs ChatModelParameters
- OpenAPITool tools: list[OpenAPITool] vs list[AnyTool]
```

Estos son warnings del type checker y no deberían causar errores en runtime.

---

## 📋 Checklist de Pruebas

Antes de usar el agente en producción, verifica lo siguiente:

- [ ] **Variables de Entorno:** Asegúrate de tener todas las variables en `.env`:
  ```
  STRAVA_CLIENT_ID=tu_client_id
  STRAVA_CLIENT_SECRET=tu_client_secret
  STRAVA_REFRESH_TOKEN=tu_refresh_token
  WATSONX_API_KEY=tu_api_key
  WATSONX_PROJECT_ID=tu_project_id
  WATSONX_URL=tu_url
  ```

- [ ] **Dependencias:** Verifica que tienes las versiones correctas:
  ```bash
  uv sync
  ```

- [ ] **Archivo YAML:** Confirma que `strava-tool.yaml` existe y es válido

- [ ] **Prueba Básica:** Ejecuta el agente con una query simple:
  ```bash
  uv run python src/beeai_agents/agent.py
  ```

- [ ] **Autenticación:** Implementa la solución para headers dinámicos antes de usar en producción

- [ ] **Manejo de Respuestas:** Verifica que `response.last_message.text` funciona correctamente

---

## 🔄 Alternativa: Usar Ollama en lugar de Watsonx

Si prefieres usar Ollama para desarrollo local:

```python
from beeai_framework.adapters.ollama import OllamaChatModel

llm = OllamaChatModel("granite4:micro")
```

**Ventajas:**
- No requiere API keys
- Más rápido para desarrollo local
- Gratis

**Requisitos:**
```bash
# Instalar Ollama
# Visita https://ollama.ai

# Descargar el modelo
ollama pull granite4:micro
```

---

## 📚 Referencias

- **Repositorio Oficial:** [i-am-bee/beeai-framework](https://github.com/i-am-bee/beeai-framework)
- **Ejemplos Python:** [python/examples/](https://github.com/i-am-bee/beeai-framework/tree/main/python/examples)
- **Ejemplo Custom Agent:** [custom_agent.py](https://github.com/i-am-bee/beeai-framework/blob/main/python/examples/agents/custom_agent.py)
- **Ejemplo OpenAPI:** [openapi.py](https://github.com/i-am-bee/beeai-framework/blob/main/python/examples/tools/openapi.py)
- **Ejemplo ReActAgent:** [agent.py](https://github.com/i-am-bee/beeai-framework/blob/main/python/examples/tools/agent.py)

---

## 🎯 Próximos Pasos Recomendados

1. **Implementar Autenticación Dinámica**
   - Investigar la API de `OpenAPITool` para headers dinámicos
   - Probar diferentes enfoques
   - Documentar la solución encontrada

2. **Pruebas Exhaustivas**
   - Probar con diferentes queries
   - Verificar que todas las operaciones de Strava funcionan
   - Validar el formato de las respuestas

3. **Optimización**
   - Ajustar parámetros del LLM según necesidades
   - Configurar memoria del agente si es necesario
   - Agregar logging para debugging

4. **Documentación**
   - Actualizar README.md con los nuevos cambios
   - Agregar ejemplos de uso
   - Documentar troubleshooting común

---

## 📝 Notas Adicionales

- El código actualizado mantiene la clase `StravaAuth` sin cambios
- La estructura general del flujo se mantiene similar
- Los comentarios en español se preservaron para mantener consistencia
- Se agregaron TODOs donde se requiere trabajo adicional

---

## ✨ Conclusión

La migración a la nueva API de BeeAI Framework está **90% completa**. El código está actualizado y debería funcionar, pero **requiere implementar la autenticación dinámica de Strava** antes de usarse en producción.

**Estado:** ✅ Listo para pruebas | ⚠️ Requiere configuración de autenticación