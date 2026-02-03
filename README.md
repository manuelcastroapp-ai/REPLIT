# SuperDevAgent

**Agente Desarrollador Avanzado de IA** — Un agente experto especializado en construir y mejorar aplicaciones de agentes de IA, sistemas multi-agente y flujos de trabajo con soporte para modelos locales y en la nube.

## 🚀 Características

- **Creación de Agentes IA**: Genera código de agentes con mejores prácticas
- **Selección de Modelos**: Recomienda modelos de IA adecuados (locales y en la nube)
- **Trazado**: Integración para depuración y monitoreo
- **Evaluación**: Framework para medir rendimiento y calidad
- **Despliegue**: Despliegue en plataformas gratuitas (Railway, Render, Vercel)
- **Modelos Locales**: Soporte para Ollama, LM Studio, HuggingFace
- **Integración con Parallels Desktop**: Gestión de máquinas virtuales
- **Orquestación Multi-Agente**: Razonamiento paralelo y agentes colaborativos

## 🛠️ Instalación

### Prerrequisitos

- Python 3.10+
- Ollama (opcional, para modelos locales)

### Instalación Rápida

```bash
# Clonar repositorio
cd SuperDevAgent

# Instalar dependencias
pip install -r requirements.txt

# Configurar entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Ejecutar agente
python main.py
```

### Configuración de Modelos Locales

```bash
# Instalar Ollama
# Visita https://ollama.ai para instrucciones

# Descargar modelo
ollama pull llama3.1

# Verificar
ollama list
```

## 📡 Uso

### API REST

El SuperDevAgent expone una API REST en `http://localhost:8000`

#### Crear Agente

```bash
POST /agents
{
  "name": "MiAgente",
  "description": "Agente para análisis de código",
  "model_type": "local",
  "capabilities": ["code_analysis", "debugging"]
}
```

#### Seleccionar Modelo

```bash
POST /models/select
{
  "task": "análisis de código Python",
  "preferences": {"local": true}
}
```

#### Añadir Trazado

```bash
POST /agents/{agent_id}/tracing
```

#### Evaluar Agente

```bash
POST /agents/evaluate
{
  "agent_id": "agent_1",
  "test_cases": [
    {"input": "def hello():", "expected": "función simple"}
  ]
}
```

#### Desplegar Agente

```bash
POST /agents/deploy
{
  "agent_id": "agent_1",
  "target": "railway"
}
```

#### Integrar Parallels

```bash
POST /parallels/integrate
{
  "vm_name": "dev-vm",
  "os": "ubuntu",
  "resources": {"cpu": 2, "ram": 4}
}
```

## 🏗️ Arquitectura

```
SuperDevAgent
├── main.py              # Servidor FastAPI principal
├── requirements.txt     # Dependencias Python
├── .env.example         # Configuración de ejemplo
├── TODO.md             # Lista de tareas
└── README.md           # Esta documentación
```

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `FOUNDRY_PROJECT_ENDPOINT` | Endpoint de Azure AI Foundry | `https://your-project.openai.azure.com/` |
| `FOUNDRY_MODEL_DEPLOYMENT_NAME` | Nombre del despliegue del modelo | `gpt-4` |
| `OLLAMA_MODEL` | Modelo local a usar | `llama3.1` |
| `PARALLELS_API_ENDPOINT` | API de Parallels Desktop | `http://localhost:8080` |

## 🧪 Desarrollo

```bash
# Ejecutar en modo desarrollo
python main.py

# Ejecutar tests
pytest

# Formatear código
black .
```

## 🚢 Despliegue

### Plataformas Soportadas

- **Railway**: `railway deploy`
- **Render**: `render deploy`
- **Vercel**: `vercel deploy`
- **Fly.io**: `fly deploy`

### Despliegue Local

```bash
# Construir imagen Docker
docker build -t superdevagent .

# Ejecutar contenedor
docker run -p 8000:8000 superdevagent
```

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

ISC License — Ver archivo LICENSE

## 🙏 Agradecimientos

- Microsoft Agent Framework
- Ollama para modelos locales
- FastAPI para la API REST
- Comunidad de IA y desarrollo

## 📞 Soporte

- **Issues**: GitHub Issues
- **Discusiones**: GitHub Discussions

---

**Construido con ❤️ para la próxima generación de desarrollo de IA**

*SuperDevAgent — El futuro del desarrollo de agentes IA*
