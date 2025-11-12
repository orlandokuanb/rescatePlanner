#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
METRICS CALCULATOR - Calculador de Mtricas de Racionalidad
Curso: MIA-103 Fundamentos de Inteligencia Artificial
Autor: Grupo de Examen Final
=============================================================================

Calcula las mtricas de racionalidad del agente planificador:
1. Eficiencia del Plan
2. Utilizacin de Recursos
3. Prioridad de Vctimas Graves
4. Costo Operacional
"""

import re
import json
from typing import List, Dict, Set, Tuple
from pathlib import Path


class MetricsCalculator:
    """
    Calculador de mtricas de racionalidad para el agente planificador.
    """
    
    # Distancias entre locaciones (en kilmetros)
    DISTANCIAS = {
        ("C0", "C1"): 10,
        ("C1", "C2"): 15,
        ("C2", "C3"): 12,
        ("C3", "M"): 8,
    }
    
    # Recursos totales disponibles
    UNIDADES_TOTALES = 6  # UM1, UM2, U1, UP, UX, U3
    PERSONAL_RESCATE_TOTAL = 4  # Mdico, 2 Rescatistas, Asistente
    PERSONAL_CONSTRUCCION_TOTAL = 21  # 6 tcnicos + 10 obreros + 1 ingeniero + 1 operador + 3 operadores
    VICTIMAS_TOTALES = 10
    VICTIMAS_GRAVES = 4
    
    def __init__(self, plan: List[str], problema_name: str = ""):
        """
        Inicializa el calculador de mtricas.
        
        Args:
            plan: Lista de acciones del plan
            problema_name: Nombre del problema para contexto
        """
        self.plan = plan
        self.problema_name = problema_name
        self.metricas: Dict = {}
        self.detalles: Dict = {}
    
    def calcular_todas_las_metricas(self) -> Dict:
        """
        Calcula todas las mtricas de racionalidad.
        
        Returns:
            Diccionario con todas las mtricas calculadas
        """
        print(f"\n{'='*80}")
        print("CLCULO DE MTRICAS DE RACIONALIDAD")
        print(f"{'='*80}")
        print(f"Plan: {len(self.plan)} acciones")
        
        metricas = {
            "problema": self.problema_name,
            "numero_acciones": len(self.plan),
        }
        
        # Mtrica 1: Eficiencia del Plan
        metricas["metrica_1_eficiencia"] = self.calcular_eficiencia()
        
        # Mtrica 2: Utilizacin de Recursos
        metricas["metrica_2_utilizacion_recursos"] = self.calcular_utilizacion_recursos()
        
        # Mtrica 3: Prioridad de Vctimas Graves
        metricas["metrica_3_prioridad_victimas"] = self.verificar_prioridad_victimas()
        
        # Mtrica 4: Costo Operacional
        metricas["metrica_4_costo_operacional"] = self.calcular_costo_operacional()
        
        # Mtricas adicionales
        metricas["acciones_por_tipo"] = self.contar_acciones_por_tipo()
        metricas["complejidad_plan"] = self.calcular_complejidad()
        
        self.metricas = metricas
        
        return metricas
    
    def calcular_eficiencia(self) -> Dict:
        """
        MTRICA 1: Eficiencia del Plan
        
        Eficiencia = AccionesMinimas / AccionesPlan
        
        Donde AccionesMinimas es una estimacin terica basada en:
        - Construccin de 3 infraestructuras
        - Transporte de personal y recursos
        - Rescate de 10 vctimas
        
        Target: >= 0.8 (mximo 20% de acciones extra)
        """
        acciones_plan = len(self.plan)
        
        # Estimacin de acciones mnimas tericas
        if "sub1" in self.problema_name:
            acciones_minimas = 15  # Transporte PPF + tcnicos + construccin + retorno
        elif "sub2" in self.problema_name:
            acciones_minimas = 30  # Ms complejo: 10 obreros + maquinaria
        elif "sub3" in self.problema_name:
            acciones_minimas = 20  # Puente colgante + operador
        elif "sub4" in self.problema_name:
            acciones_minimas = 35  # Rescate de 10 vctimas
        else:
            # Problema completo
            acciones_minimas = 100  # 15 + 30 + 20 + 35
        
        eficiencia = min(acciones_minimas / acciones_plan, 1.0) if acciones_plan > 0 else 0.0
        porcentaje_eficiencia = eficiencia * 100
        
        # Evaluacin
        if eficiencia >= 0.8:
            evaluacion = "EXCELENTE"
        elif eficiencia >= 0.6:
            evaluacion = "BUENO"
        elif eficiencia >= 0.4:
            evaluacion = "ACEPTABLE"
        else:
            evaluacion = "MEJORABLE"
        
        print(f"\n MTRICA 1: Eficiencia del Plan")
        print(f"   Acciones mnimas tericas: {acciones_minimas}")
        print(f"   Acciones en el plan: {acciones_plan}")
        print(f"   Eficiencia: {porcentaje_eficiencia:.1f}%")
        print(f"   Evaluacin: {evaluacion}")
        
        return {
            "acciones_minimas_teoricas": acciones_minimas,
            "acciones_plan": acciones_plan,
            "eficiencia": round(eficiencia, 3),
            "porcentaje": round(porcentaje_eficiencia, 1),
            "evaluacion": evaluacion,
            "cumple_target": eficiencia >= 0.8
        }
    
    def calcular_utilizacion_recursos(self) -> Dict:
        """
        MTRICA 2: Utilizacin de Recursos
        
        Utilizacin = (RecursosUsados / RecursosDisponibles)  100
        
        Considera:
        - Unidades mviles utilizadas
        - Personal de rescate utilizado
        - Personal de construccin utilizado
        
        Target: 80-95% (ni subutilizacin ni sobreutilizacin)
        """
        # Extraer recursos usados del plan
        unidades_usadas = self._extraer_unidades_usadas()
        personal_rescate = self._extraer_personal_rescate()
        personal_construccion = self._extraer_personal_construccion()
        
        # Calcular totales
        recursos_usados = len(unidades_usadas) + len(personal_rescate) + len(personal_construccion)
        recursos_disponibles = (
            self.UNIDADES_TOTALES + 
            self.PERSONAL_RESCATE_TOTAL + 
            self.PERSONAL_CONSTRUCCION_TOTAL
        )
        
        utilizacion = (recursos_usados / recursos_disponibles) * 100 if recursos_disponibles > 0 else 0
        
        # Evaluacin
        if 80 <= utilizacion <= 95:
            evaluacion = "PTIMO"
        elif 60 <= utilizacion < 80:
            evaluacion = "BUENO"
        elif utilizacion > 95:
            evaluacion = "SOBREUTILIZACIN"
        else:
            evaluacion = "SUBUTILIZACIN"
        
        print(f"\n MTRICA 2: Utilizacin de Recursos")
        print(f"   Unidades mviles usadas: {len(unidades_usadas)}/{self.UNIDADES_TOTALES}")
        print(f"   Personal rescate usado: {len(personal_rescate)}/{self.PERSONAL_RESCATE_TOTAL}")
        print(f"   Personal construccin usado: {len(personal_construccion)}/{self.PERSONAL_CONSTRUCCION_TOTAL}")
        print(f"   Utilizacin total: {utilizacion:.1f}%")
        print(f"   Evaluacin: {evaluacion}")
        
        return {
            "unidades_usadas": list(unidades_usadas),
            "personal_rescate_usado": list(personal_rescate),
            "personal_construccion_usado": list(personal_construccion),
            "recursos_usados": recursos_usados,
            "recursos_disponibles": recursos_disponibles,
            "porcentaje_utilizacion": round(utilizacion, 1),
            "evaluacion": evaluacion,
            "cumple_target": 80 <= utilizacion <= 95
        }
    
    def verificar_prioridad_victimas(self) -> Dict:
        """
        MTRICA 3: Prioridad de Vctimas Graves
        
        Verifica que TODAS las vctimas graves sean estabilizadas ANTES
        que cualquier otra vctima sea evacuada.
        
        Prioridad = (GravesAtendidasPrimero / TotalGraves)  100
        
        Target: 100% (CRTICO)
        """
        # Buscar acciones de estabilizacin y rescate
        indices_estabilizacion = []
        indices_rescate_graves = []
        indices_rescate_otras = []
        
        for i, accion in enumerate(self.plan):
            accion_upper = accion.upper()
            
            # Detectar estabilizacin de vctimas graves
            if "ESTABILIZAR" in accion_upper:
                if any(f"VG{j}" in accion_upper for j in range(1, 5)):
                    indices_estabilizacion.append(i)
            
            # Detectar carga/rescate de vctimas
            if "CARGAR_PERSONA" in accion_upper or "REGISTRAR_RESCATE" in accion_upper:
                if any(f"VG{j}" in accion_upper for j in range(1, 5)):
                    indices_rescate_graves.append(i)
                elif any(f"VE{j}" in accion_upper for j in range(1, 4)):
                    indices_rescate_otras.append(i)
                elif any(f"VNA{j}" in accion_upper for j in range(1, 4)):
                    indices_rescate_otras.append(i)
        
        # Verificar prioridad
        victimas_graves_atendidas = len(indices_estabilizacion)
        prioridad_correcta = True
        
        if indices_estabilizacion and indices_rescate_otras:
            ultima_estabilizacion = max(indices_estabilizacion)
            primera_otra = min(indices_rescate_otras)
            prioridad_correcta = ultima_estabilizacion < primera_otra
        
        porcentaje_prioridad = 100.0 if prioridad_correcta else 0.0
        
        evaluacion = "CORRECTO" if prioridad_correcta else "INCORRECTO - PRIORIDAD VIOLADA"
        
        print(f"\n MTRICA 3: Prioridad de Vctimas Graves")
        print(f"   Vctimas graves estabilizadas: {victimas_graves_atendidas}")
        print(f"   Prioridad respetada: {'S' if prioridad_correcta else 'NO'}")
        print(f"   Porcentaje: {porcentaje_prioridad:.1f}%")
        print(f"   Evaluacin: {evaluacion}")
        
        return {
            "victimas_graves_atendidas": victimas_graves_atendidas,
            "total_victimas_graves": self.VICTIMAS_GRAVES,
            "prioridad_respetada": prioridad_correcta,
            "porcentaje": round(porcentaje_prioridad, 1),
            "evaluacion": evaluacion,
            "cumple_target": prioridad_correcta
        }
    
    def calcular_costo_operacional(self) -> Dict:
        """
        MTRICA 4: Costo Operacional
        
        Costo = (NumViajes  Distancia)
        
        Calcula el costo total en kilmetros recorridos por todas las unidades.
        
        Target: Minimizar (comparar con cota superior terica)
        """
        costo_total_km = 0.0
        viajes_detalle = []
        
        # Analizar cada accin de traslado
        for accion in self.plan:
            if "TRASLADAR_UNIDAD" in accion.upper():
                # Extraer origen y destino
                partes = accion.split()
                if len(partes) >= 4:
                    unidad = partes[1] if len(partes) > 1 else "?"
                    origen = partes[2] if len(partes) > 2 else "?"
                    destino = partes[3] if len(partes) > 3 else "?"
                    
                    # Buscar distancia
                    distancia = self._obtener_distancia(origen, destino)
                    
                    if distancia > 0:
                        costo_total_km += distancia
                        viajes_detalle.append({
                            "unidad": unidad,
                            "origen": origen,
                            "destino": destino,
                            "distancia_km": distancia
                        })
        
        # Cota superior terica (peor caso)
        # Cada unidad hace viaje completo ida y vuelta: 6 unidades  (10+15+12+8)  2 = 540 km
        cota_superior = 540
        eficiencia_costo = (cota_superior - costo_total_km) / cota_superior * 100 if cota_superior > 0 else 0
        
        print(f"\n MTRICA 4: Costo Operacional")
        print(f"   Total de viajes: {len(viajes_detalle)}")
        print(f"   Costo total: {costo_total_km:.1f} km")
        print(f"   Cota superior: {cota_superior} km")
        print(f"   Eficiencia de costo: {eficiencia_costo:.1f}%")
        
        return {
            "numero_viajes": len(viajes_detalle),
            "costo_total_km": round(costo_total_km, 1),
            "cota_superior_km": cota_superior,
            "eficiencia_costo": round(eficiencia_costo, 1),
            "viajes": viajes_detalle[:10]  # Primeros 10 para no saturar
        }
    
    def contar_acciones_por_tipo(self) -> Dict:
        """
        Cuenta cuntas acciones de cada tipo hay en el plan.
        """
        conteo = {}
        
        for accion in self.plan:
            # Extraer el tipo de accin (primera palabra)
            tipo = accion.split()[0].upper() if accion.split() else "DESCONOCIDO"
            conteo[tipo] = conteo.get(tipo, 0) + 1
        
        return conteo
    
    def calcular_complejidad(self) -> Dict:
        """
        Calcula mtricas de complejidad del plan.
        """
        # Nmero de locaciones visitadas
        locaciones = set()
        for accion in self.plan:
            for loc in ["C0", "C1", "C2", "C3", "M"]:
                if loc in accion.upper():
                    locaciones.add(loc)
        
        return {
            "locaciones_visitadas": len(locaciones),
            "promedio_acciones_por_locacion": round(len(self.plan) / len(locaciones), 1) if locaciones else 0
        }
    
    def _extraer_unidades_usadas(self) -> Set[str]:
        """Extrae unidades mviles usadas en el plan."""
        unidades = set()
        unidades_posibles = ["UM1", "UM2", "U1", "UP", "UX", "U3"]
        
        for accion in self.plan:
            accion_upper = accion.upper()
            for u in unidades_posibles:
                if u in accion_upper:
                    unidades.add(u)
        
        return unidades
    
    def _extraer_personal_rescate(self) -> Set[str]:
        """Extrae personal de rescate usado en el plan."""
        personal = set()
        keywords = ["MEDICO", "RESCATISTA", "ASISTENTE"]
        
        for accion in self.plan:
            accion_upper = accion.upper()
            for kw in keywords:
                if kw in accion_upper:
                    # Extraer nombre especfico
                    partes = accion.split()
                    for p in partes:
                        if kw in p.upper():
                            personal.add(p)
        
        return personal
    
    def _extraer_personal_construccion(self) -> Set[str]:
        """Extrae personal de construccin usado en el plan."""
        personal = set()
        keywords = ["TECNICO", "OBRERO", "INGENIERO", "OPERADOR"]
        
        for accion in self.plan:
            accion_upper = accion.upper()
            for kw in keywords:
                if kw in accion_upper:
                    partes = accion.split()
                    for p in partes:
                        if kw in p.upper():
                            personal.add(p)
        
        return personal
    
    def _obtener_distancia(self, origen: str, destino: str) -> float:
        """Obtiene la distancia entre dos locaciones."""
        # Buscar en ambas direcciones (es simtrica)
        for (o, d), dist in self.DISTANCIAS.items():
            if (o == origen and d == destino) or (o == destino and d == origen):
                return dist
        return 0.0
    
    def generar_reporte(self, archivo: str = None) -> str:
        """
        Genera un reporte completo de las mtricas.
        
        Args:
            archivo: Ruta donde guardar el reporte
            
        Returns:
            String con el reporte
        """
        if not self.metricas:
            self.calcular_todas_las_metricas()
        
        lineas = []
        lineas.append("\n" + "="*80)
        lineas.append("REPORTE DE MTRICAS DE RACIONALIDAD")
        lineas.append("="*80)
        lineas.append(f"\nProblema: {self.problema_name}")
        lineas.append(f"Nmero de acciones: {len(self.plan)}")
        
        lineas.append("\n" + "-"*80)
        lineas.append("RESUMEN DE MTRICAS")
        lineas.append("-"*80)
        
        # Mtrica 1
        m1 = self.metricas.get("metrica_1_eficiencia", {})
        lineas.append(f"\n1. EFICIENCIA DEL PLAN: {m1.get('porcentaje', 0):.1f}%")
        lineas.append(f"   Evaluacin: {m1.get('evaluacion', 'N/A')}")
        lineas.append(f"   Cumple target: {' S' if m1.get('cumple_target') else ' NO'}")
        
        # Mtrica 2
        m2 = self.metricas.get("metrica_2_utilizacion_recursos", {})
        lineas.append(f"\n2. UTILIZACIN DE RECURSOS: {m2.get('porcentaje_utilizacion', 0):.1f}%")
        lineas.append(f"   Evaluacin: {m2.get('evaluacion', 'N/A')}")
        lineas.append(f"   Cumple target: {' S' if m2.get('cumple_target') else ' NO'}")
        
        # Mtrica 3
        m3 = self.metricas.get("metrica_3_prioridad_victimas", {})
        lineas.append(f"\n3. PRIORIDAD VCTIMAS GRAVES: {m3.get('porcentaje', 0):.1f}%")
        lineas.append(f"   Evaluacin: {m3.get('evaluacion', 'N/A')}")
        lineas.append(f"   Cumple target: {' S' if m3.get('cumple_target') else ' NO'}")
        
        # Mtrica 4
        m4 = self.metricas.get("metrica_4_costo_operacional", {})
        lineas.append(f"\n4. COSTO OPERACIONAL: {m4.get('costo_total_km', 0):.1f} km")
        lineas.append(f"   Eficiencia: {m4.get('eficiencia_costo', 0):.1f}%")
        
        lineas.append("\n" + "="*80)
        
        reporte = "\n".join(lineas)
        
        if archivo:
            Path(archivo).parent.mkdir(parents=True, exist_ok=True)
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write(reporte)
            print(f"\n Reporte guardado en: {archivo}")
        
        return reporte
    
    def exportar_json(self, archivo: str):
        """
        Exporta las mtricas en formato JSON.
        """
        if not self.metricas:
            self.calcular_todas_las_metricas()
        
        Path(archivo).parent.mkdir(parents=True, exist_ok=True)
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(self.metricas, f, indent=2, ensure_ascii=False)
        
        print(f" Mtricas JSON guardadas en: {archivo}")


def main():
    """Funcin de prueba."""
    # Plan de ejemplo
    plan_ejemplo = [
        "CARGAR_RECURSO PPF U1 C0",
        "CARGAR_PERSONA TecnicoC1_1 U1 C0",
        "TRASLADAR_UNIDAD U1 C0 C1",
        "DESCARGAR_RECURSO PPF U1 C1",
        "CONSTRUIR_PUENTE_PPF PPF C1 C2 TecnicoC1_1 TecnicoC1_2 TecnicoC1_3",
    ]
    
    calc = MetricsCalculator(plan_ejemplo, "sub1_puente_c1")
    metricas = calc.calcular_todas_las_metricas()
    print(calc.generar_reporte())
    
    return 0


if __name__ == "__main__":
    main()

