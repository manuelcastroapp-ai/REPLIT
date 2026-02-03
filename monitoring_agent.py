"""
Agente de monitoreo para SuperDevAgent

Proporciona funcionalidades de trazado, métricas y alertas.
"""

import time
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict

class MonitoringAgent:
    """Agente de monitoreo con trazado, métricas y alertas"""

    def __init__(self):
        self.traces: Dict[str, List[Dict[str, Any]]] = {}
        self.metrics: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.alerts: List[Dict[str, Any]] = []
        self.active_traces: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()

    def start_trace(self, trace_id: str, name: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Iniciar un nuevo trazado"""
        with self.lock:
            trace = {
                "id": trace_id,
                "name": name,
                "start_time": datetime.utcnow(),
                "end_time": None,
                "duration": None,
                "steps": [],
                "metadata": metadata or {},
                "status": "running"
            }
            self.active_traces[trace_id] = trace
            self.traces[trace_id] = [trace]
            return trace_id

    def add_trace_step(self, trace_id: str, step_name: str, data: Optional[Dict[str, Any]] = None):
        """Añadir un paso al trazado"""
        with self.lock:
            if trace_id in self.active_traces:
                step = {
                    "name": step_name,
                    "timestamp": datetime.utcnow(),
                    "data": data or {}
                }
                self.active_traces[trace_id]["steps"].append(step)

    def end_trace(self, trace_id: str, result: Optional[Dict[str, Any]] = None):
        """Finalizar un trazado"""
        with self.lock:
            if trace_id in self.active_traces:
                trace = self.active_traces[trace_id]
                trace["end_time"] = datetime.utcnow()
                trace["duration"] = (trace["end_time"] - trace["start_time"]).total_seconds()
                trace["status"] = "completed"
                trace["result"] = result or {}

                # Mover a trazados completados
                if trace_id in self.traces:
                    self.traces[trace_id].append(trace)
                else:
                    self.traces[trace_id] = [trace]

                del self.active_traces[trace_id]

    def record_metric(self, name: str, value: Any, tags: Optional[Dict[str, str]] = None):
        """Registrar una métrica"""
        with self.lock:
            metric = {
                "name": name,
                "value": value,
                "timestamp": datetime.utcnow(),
                "tags": tags or {}
            }
            self.metrics[name].append(metric)

    def get_metrics(self, name: Optional[str] = None, hours: int = 24) -> Dict[str, List[Dict[str, Any]]]:
        """Obtener métricas"""
        with self.lock:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)

            if name:
                return {
                    name: [m for m in self.metrics[name] if m["timestamp"] > cutoff_time]
                }
            else:
                result = {}
                for metric_name, metric_list in self.metrics.items():
                    result[metric_name] = [m for m in metric_list if m["timestamp"] > cutoff_time]
                return result

    def get_traces(self, trace_id: Optional[str] = None, hours: int = 24) -> Dict[str, List[Dict[str, Any]]]:
        """Obtener trazados"""
        with self.lock:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)

            if trace_id:
                if trace_id in self.traces:
                    return {
                        trace_id: [t for t in self.traces[trace_id]
                                 if t.get("start_time", datetime.min) > cutoff_time]
                    }
                else:
                    return {}
            else:
                result = {}
                for tid, trace_list in self.traces.items():
                    filtered_traces = [t for t in trace_list
                                     if t.get("start_time", datetime.min) > cutoff_time]
                    if filtered_traces:
                        result[tid] = filtered_traces
                return result

    def create_alert(self, alert_type: str, message: str, severity: str = "info",
                    metadata: Optional[Dict[str, Any]] = None):
        """Crear una alerta"""
        with self.lock:
            alert = {
                "id": f"alert_{int(time.time())}_{len(self.alerts)}",
                "type": alert_type,
                "message": message,
                "severity": severity,
                "timestamp": datetime.utcnow(),
                "metadata": metadata or {},
                "acknowledged": False
            }
            self.alerts.append(alert)
            return alert["id"]

    def get_alerts(self, acknowledged: Optional[bool] = None, hours: int = 24) -> List[Dict[str, Any]]:
        """Obtener alertas"""
        with self.lock:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)

            alerts = [a for a in self.alerts if a["timestamp"] > cutoff_time]

            if acknowledged is not None:
                alerts = [a for a in alerts if a["acknowledged"] == acknowledged]

            return alerts

    def acknowledge_alert(self, alert_id: str):
        """Marcar alerta como reconocida"""
        with self.lock:
            for alert in self.alerts:
                if alert["id"] == alert_id:
                    alert["acknowledged"] = True
                    break

    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del sistema de monitoreo"""
        with self.lock:
            total_traces = sum(len(traces) for traces in self.traces.values())
            active_traces = len(self.active_traces)
            total_metrics = sum(len(metrics) for metrics in self.metrics.values())
            total_alerts = len(self.alerts)
            unacknowledged_alerts = len([a for a in self.alerts if not a["acknowledged"]])

            return {
                "total_traces": total_traces,
                "active_traces": active_traces,
                "total_metrics": total_metrics,
                "total_alerts": total_alerts,
                "unacknowledged_alerts": unacknowledged_alerts,
                "timestamp": datetime.utcnow()
            }
