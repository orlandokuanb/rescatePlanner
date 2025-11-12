#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba rápida del planificador
"""

import sys
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rescate_planner import RescatePlanner
from metrics_calculator import MetricsCalculator

def main():
    print("="*80)
    print("PRUEBA RAPIDA - PLANIFICADOR DE RESCATE")
    print("="*80)
    
    # Configuración
    dominio = "pddl/dominio_rescate.pddl"
    problema = "pddl/subproblemas/sub1_puente_c1.pddl"
    
    print(f"\nDominio: {dominio}")
    print(f"Problema: {problema}")
    
    try:
        # Crear planificador
        planner = RescatePlanner(dominio, problema, "auto")
        
        # Ejecutar
        plan = planner.ejecutar_planificador(timeout=300)
        
        if plan:
            print("\n" + "="*80)
            print("EXITO - Plan generado")
            print("="*80)
            print(f"\nNumero de acciones: {len(plan)}")
            print("\nPrimeras 5 acciones:")
            for i, accion in enumerate(plan[:5], 1):
                print(f"  {i}. {accion}")
            
            if len(plan) > 5:
                print(f"  ... ({len(plan)-5} acciones mas)")
            
            # Calcular metricas
            print("\n" + "-"*80)
            print("Calculando metricas...")
            print("-"*80)
            calc = MetricsCalculator(plan, "sub1")
            metricas = calc.calcular_todas_las_metricas()
            
            print("\nRESUMEN DE METRICAS:")
            print(f"  Eficiencia: {metricas['metrica_1_eficiencia']['porcentaje']:.1f}%")
            print(f"  Utilizacion: {metricas['metrica_2_utilizacion_recursos']['porcentaje_utilizacion']:.1f}%")
            print(f"  Prioridad: {metricas['metrica_3_prioridad_victimas']['porcentaje']:.1f}%")
            print(f"  Costo: {metricas['metrica_4_costo_operacional']['costo_total_km']:.1f} km")
            
            return 0
        else:
            print("\n" + "="*80)
            print("ERROR - No se pudo generar plan")
            print("="*80)
            return 1
            
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

