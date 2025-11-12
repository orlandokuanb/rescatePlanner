#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
EJECUTAR EXAMEN - Script Principal
Curso: MIA-103 Fundamentos de Inteligencia Artificial
Examen Final: Planificación Automatizada en Espacio de Estados
=============================================================================

Script principal que ejecuta el sistema completo de planificación y análisis.
"""

import sys
import os
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rescate_planner import RescatePlanner
from metrics_calculator import MetricsCalculator


def imprimir_header():
    """Imprime el encabezado del sistema."""
    print("\n" + "="*80)
    print("  SISTEMA DE PLANIFICACIÓN AUTOMATIZADA - RESCATE EN MINA")
    print("  Fundamentos de Inteligencia Artificial (MIA-103)")
    print("  Examen Final 2025-2")
    print("="*80)


def ejecutar_subproblema(numero: int, dominio: str, problema: str, timeout: int = 300):
    """
    Ejecuta un sub-problema específico.
    
    Args:
        numero: Número del sub-problema (1-4)
        dominio: Ruta al archivo de dominio
        problema: Ruta al archivo de problema
        timeout: Tiempo máximo en segundos
    
    Returns:
        Tuple (plan, metricas) o (None, None) si falla
    """
    print(f"\n{'='*80}")
    print(f"  SUB-PROBLEMA {numero}")
    print(f"{'='*80}")
    
    descripcion = {
        1: "Construcción de Puente en C1",
        2: "Construcción de Carretera en C2",
        3: "Instalación de Puente Colgante en C3",
        4: "Rescate de Víctimas",
    }
    
    print(f"\nObjetivo: {descripcion.get(numero, 'Desconocido')}")
    print(f"Archivo: {Path(problema).name}")
    
    try:
        # Crear planificador
        planner = RescatePlanner(dominio, problema, "auto")
        
        # Ejecutar planificación
        plan = planner.ejecutar_planificador(timeout=timeout)
        
        if not plan:
            print(f"\n❌ No se pudo generar plan para sub-problema {numero}")
            return None, None
        
        # Visualizar plan
        print(planner.visualizar_plan(guardar_archivo=True))
        
        # Calcular métricas
        calc = MetricsCalculator(plan, Path(problema).stem)
        metricas = calc.calcular_todas_las_metricas()
        
        # Generar reportes
        calc.generar_reporte(
            archivo=f"experimentos/resultados/sub{numero}_reporte_metricas.txt"
        )
        calc.exportar_json(
            archivo=f"experimentos/resultados/sub{numero}_metricas.json"
        )
        
        # Guardar estadísticas del planificador
        planner.guardar_estadisticas(
            archivo=f"experimentos/resultados/sub{numero}_stats.json"
        )
        
        return plan, metricas
        
    except Exception as e:
        print(f"\n❌ Error ejecutando sub-problema {numero}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None


def ejecutar_problema_completo(dominio: str, problema: str, timeout: int = 600):
    """
    Ejecuta el problema completo.
    
    Args:
        dominio: Ruta al archivo de dominio
        problema: Ruta al archivo de problema
        timeout: Tiempo máximo en segundos
    
    Returns:
        Tuple (plan, metricas) o (None, None) si falla
    """
    print(f"\n{'='*80}")
    print(f"  PROBLEMA COMPLETO - RESCATE INTEGRAL")
    print(f"{'='*80}")
    
    print("\nObjetivo: Construir toda la infraestructura Y rescatar 10 víctimas")
    print(f"Archivo: {Path(problema).name}")
    
    try:
        # Crear planificador
        planner = RescatePlanner(dominio, problema, "auto")
        
        # Ejecutar planificación
        plan = planner.ejecutar_planificador(timeout=timeout)
        
        if not plan:
            print(f"\n❌ No se pudo generar plan para el problema completo")
            return None, None
        
        # Visualizar plan
        print(planner.visualizar_plan(guardar_archivo=True))
        
        # Calcular métricas
        calc = MetricsCalculator(plan, Path(problema).stem)
        metricas = calc.calcular_todas_las_metricas()
        
        # Generar reportes
        calc.generar_reporte(
            archivo="experimentos/resultados/completo_reporte_metricas.txt"
        )
        calc.exportar_json(
            archivo="experimentos/resultados/completo_metricas.json"
        )
        
        # Guardar estadísticas del planificador
        planner.guardar_estadisticas(
            archivo="experimentos/resultados/completo_stats.json"
        )
        
        return plan, metricas
        
    except Exception as e:
        print(f"\n❌ Error ejecutando problema completo: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None


def generar_resumen_global(resultados_sub: list, resultado_completo: tuple):
    """
    Genera un resumen global de todos los resultados.
    
    Args:
        resultados_sub: Lista de tuplas (plan, metricas) de sub-problemas
        resultado_completo: Tupla (plan, metricas) del problema completo
    """
    print(f"\n{'='*80}")
    print("  RESUMEN GLOBAL DE RESULTADOS")
    print(f"{'='*80}")
    
    lineas = []
    lineas.append("\n" + "="*80)
    lineas.append("RESUMEN GLOBAL - EXAMEN FINAL MIA-103")
    lineas.append("="*80)
    
    # Resumen de sub-problemas
    lineas.append("\n--- SUB-PROBLEMAS ---")
    for i, (plan, metricas) in enumerate(resultados_sub, 1):
        if plan and metricas:
            lineas.append(f"\nSub-problema {i}: ✅ EXITOSO")
            lineas.append(f"  Acciones: {len(plan)}")
            
            # Extraer métricas clave
            m1 = metricas.get('metrica_1_eficiencia', {})
            lineas.append(f"  Eficiencia: {m1.get('porcentaje', 0):.1f}%")
        else:
            lineas.append(f"\nSub-problema {i}: ❌ FALLIDO")
    
    # Problema completo
    lineas.append("\n--- PROBLEMA COMPLETO ---")
    plan_completo, metricas_completo = resultado_completo
    
    if plan_completo and metricas_completo:
        lineas.append("✅ EXITOSO")
        lineas.append(f"Acciones totales: {len(plan_completo)}")
        
        m1 = metricas_completo.get('metrica_1_eficiencia', {})
        m2 = metricas_completo.get('metrica_2_utilizacion_recursos', {})
        m3 = metricas_completo.get('metrica_3_prioridad_victimas', {})
        m4 = metricas_completo.get('metrica_4_costo_operacional', {})
        
        lineas.append(f"\nMÉTRICAS FINALES:")
        lineas.append(f"  1. Eficiencia: {m1.get('porcentaje', 0):.1f}% - {m1.get('evaluacion', 'N/A')}")
        lineas.append(f"  2. Utilización: {m2.get('porcentaje_utilizacion', 0):.1f}% - {m2.get('evaluacion', 'N/A')}")
        lineas.append(f"  3. Prioridad: {m3.get('porcentaje', 0):.1f}% - {m3.get('evaluacion', 'N/A')}")
        lineas.append(f"  4. Costo: {m4.get('costo_total_km', 0):.1f} km")
        
        # Evaluación global
        targets_cumplidos = sum([
            m1.get('cumple_target', False),
            m2.get('cumple_target', False),
            m3.get('cumple_target', False),
        ])
        
        lineas.append(f"\nTARGETS CUMPLIDOS: {targets_cumplidos}/3")
        
        if targets_cumplidos == 3:
            evaluacion_global = "EXCELENTE - Todos los targets cumplidos"
        elif targets_cumplidos >= 2:
            evaluacion_global = "BUENO - Mayoría de targets cumplidos"
        elif targets_cumplidos >= 1:
            evaluacion_global = "ACEPTABLE - Algunos targets cumplidos"
        else:
            evaluacion_global = "MEJORABLE - Targets no cumplidos"
        
        lineas.append(f"EVALUACIÓN GLOBAL: {evaluacion_global}")
    else:
        lineas.append("❌ FALLIDO")
    
    lineas.append("\n" + "="*80)
    
    resumen = "\n".join(lineas)
    print(resumen)
    
    # Guardar resumen
    with open("experimentos/resultados/RESUMEN_GLOBAL.txt", 'w', encoding='utf-8') as f:
        f.write(resumen)
    
    print(f"\n📄 Resumen guardado en: experimentos/resultados/RESUMEN_GLOBAL.txt")


def main():
    """
    Función principal del sistema.
    """
    imprimir_header()
    
    # Configuración de rutas
    dominio = "pddl/dominio_rescate.pddl"
    
    subproblemas = [
        "pddl/subproblemas/sub1_puente_c1.pddl",
        "pddl/subproblemas/sub2_carretera_c2.pddl",
        "pddl/subproblemas/sub3_puente_c3.pddl",
        "pddl/subproblemas/sub4_rescate_solo.pddl",
    ]
    
    problema_completo = "pddl/problema_rescate.pddl"
    
    # Verificar que existan los archivos
    if not Path(dominio).exists():
        print(f"\n❌ ERROR: No se encontró el archivo de dominio: {dominio}")
        return 1
    
    print(f"\n✅ Dominio encontrado: {dominio}")
    print(f"✅ {len(subproblemas)} sub-problemas configurados")
    print(f"✅ Problema completo: {problema_completo}")
    
    # Menú de opciones
    print(f"\n{'='*80}")
    print("OPCIONES DE EJECUCIÓN:")
    print("="*80)
    print("1. Ejecutar sub-problema 1 (Puente C1)")
    print("2. Ejecutar sub-problema 2 (Carretera C2)")
    print("3. Ejecutar sub-problema 3 (Puente Colgante C3)")
    print("4. Ejecutar sub-problema 4 (Rescate)")
    print("5. Ejecutar todos los sub-problemas")
    print("6. Ejecutar problema completo")
    print("7. Ejecutar TODO (sub-problemas + completo)")
    print("0. Salir")
    
    try:
        opcion = input("\nSeleccione una opción (0-7): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\nEjecución interrumpida por el usuario.")
        return 0
    
    resultados_sub = [None, None, None, None]
    resultado_completo = (None, None)
    
    if opcion == "1":
        resultados_sub[0] = ejecutar_subproblema(1, dominio, subproblemas[0])
    
    elif opcion == "2":
        resultados_sub[1] = ejecutar_subproblema(2, dominio, subproblemas[1])
    
    elif opcion == "3":
        resultados_sub[2] = ejecutar_subproblema(3, dominio, subproblemas[2])
    
    elif opcion == "4":
        resultados_sub[3] = ejecutar_subproblema(4, dominio, subproblemas[3])
    
    elif opcion == "5":
        for i in range(4):
            resultados_sub[i] = ejecutar_subproblema(i+1, dominio, subproblemas[i])
    
    elif opcion == "6":
        resultado_completo = ejecutar_problema_completo(dominio, problema_completo)
    
    elif opcion == "7":
        # Ejecutar todo
        for i in range(4):
            resultados_sub[i] = ejecutar_subproblema(i+1, dominio, subproblemas[i])
        
        resultado_completo = ejecutar_problema_completo(dominio, problema_completo)
        
        # Generar resumen global
        generar_resumen_global(resultados_sub, resultado_completo)
    
    elif opcion == "0":
        print("\nSaliendo...")
        return 0
    
    else:
        print(f"\n❌ Opción inválida: {opcion}")
        return 1
    
    print(f"\n{'='*80}")
    print("  EJECUCIÓN COMPLETADA")
    print(f"{'='*80}")
    print("\n📁 Revisa los resultados en: experimentos/resultados/")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

