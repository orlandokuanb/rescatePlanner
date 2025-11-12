#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
VALIDADOR DEL SISTEMA - Verifica que todo esté correcto
=============================================================================
"""

import sys
from pathlib import Path
import json


def validar_archivos():
    """Valida que todos los archivos necesarios existan."""
    print("\n" + "="*80)
    print("VALIDANDO SISTEMA DE PLANIFICACIÓN")
    print("="*80)
    
    errores = []
    warnings = []
    
    # Archivos PDDL críticos
    archivos_pddl = [
        "pddl/dominio_rescate.pddl",
        "pddl/problema_rescate.pddl",
        "pddl/subproblemas/sub1_puente_c1.pddl",
        "pddl/subproblemas/sub2_carretera_c2.pddl",
        "pddl/subproblemas/sub3_puente_c3.pddl",
        "pddl/subproblemas/sub4_rescate_solo.pddl",
    ]
    
    print("\n[*] Validando archivos PDDL...")
    for archivo in archivos_pddl:
        ruta = Path(archivo)
        if ruta.exists():
            tamaño = ruta.stat().st_size / 1024
            print(f"  [OK] {archivo} ({tamaño:.1f} KB)")
        else:
            errores.append(f"  [ERROR] FALTA: {archivo}")
            print(errores[-1])
    
    # Archivos Python
    archivos_python = [
        "src/rescate_planner.py",
        "src/metrics_calculator.py",
        "ejecutar_examen.py",
    ]
    
    print("\n[*] Validando archivos Python...")
    for archivo in archivos_python:
        ruta = Path(archivo)
        if ruta.exists():
            tamaño = ruta.stat().st_size / 1024
            print(f"  [OK] {archivo} ({tamaño:.1f} KB)")
            
            # Verificar sintaxis
            try:
                with open(ruta, 'r', encoding='utf-8') as f:
                    compile(f.read(), ruta.name, 'exec')
                print(f"     [+] Sintaxis valida")
            except SyntaxError as e:
                errores.append(f"  [ERROR] ERROR DE SINTAXIS en {archivo}: {e}")
                print(errores[-1])
        else:
            errores.append(f"  [ERROR] FALTA: {archivo}")
            print(errores[-1])
    
    # Ontología
    archivos_ontologia = [
        "conceptos.json",
        "relaciones.json",
        "atributos.json",
        "red_semantica.dot",
    ]
    
    print("\n[*] Validando ontologia...")
    for archivo in archivos_ontologia:
        ruta = Path(archivo)
        if ruta.exists():
            tamaño = ruta.stat().st_size / 1024
            print(f"  [OK] {archivo} ({tamaño:.1f} KB)")
            
            # Validar JSON
            if archivo.endswith('.json'):
                try:
                    with open(ruta, 'r', encoding='utf-8') as f:
                        json.load(f)
                    print(f"     [+] JSON valido")
                except json.JSONDecodeError as e:
                    warnings.append(f"  [WARN] JSON invalido en {archivo}: {e}")
                    print(warnings[-1])
        else:
            warnings.append(f"  [WARN] Falta (opcional): {archivo}")
            print(warnings[-1])
    
    # Directorios
    print("\n[*] Validando estructura de directorios...")
    directorios = [
        "pddl",
        "pddl/subproblemas",
        "src",
        "experimentos",
        "experimentos/resultados",
    ]
    
    for directorio in directorios:
        ruta = Path(directorio)
        if ruta.exists() and ruta.is_dir():
            print(f"  [OK] {directorio}/")
        else:
            print(f"  [INFO] Creando {directorio}/")
            ruta.mkdir(parents=True, exist_ok=True)
    
    # Verificar Python
    print("\n[*] Validando entorno Python...")
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print(f"  [OK] Version compatible")
    else:
        errores.append(f"  [ERROR] Se requiere Python 3.8 o superior")
        print(errores[-1])
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE VALIDACION")
    print("="*80)
    
    if not errores:
        print("\n[OK] SISTEMA VALIDO - Todos los archivos criticos presentes")
        print("[OK] Sintaxis correcta en todos los archivos Python")
        print("[OK] Estructura de directorios completa")
        
        if warnings:
            print(f"\n[WARN] {len(warnings)} advertencias (no criticas)")
        
        print("\n[LISTO] El sistema esta listo para ejecutarse")
        print("\nEjecuta: python ejecutar_examen.py")
        
        return 0
    else:
        print(f"\n[ERROR] {len(errores)} ERRORES CRITICOS encontrados:")
        for error in errores:
            print(error)
        
        print("\n[WARN] Corrige los errores antes de continuar")
        return 1


def validar_pddl_sintaxis():
    """Validación básica de sintaxis PDDL."""
    print("\n" + "-"*80)
    print("VALIDACION BASICA DE SINTAXIS PDDL")
    print("-"*80)
    
    dominio = Path("pddl/dominio_rescate.pddl")
    
    if not dominio.exists():
        print("[ERROR] Dominio no encontrado")
        return False
    
    try:
        with open(dominio, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificaciones básicas
        checks = [
            ("(define (domain", "Define de dominio"),
            (":requirements", "Requirements"),
            (":types", "Types"),
            (":predicates", "Predicates"),
            (":action", "Al menos una accion"),
        ]
        
        for patron, nombre in checks:
            if patron in contenido:
                print(f"  [OK] {nombre}")
            else:
                print(f"  [WARN] Falta: {nombre}")
        
        # Contar paréntesis
        abiertos = contenido.count('(')
        cerrados = contenido.count(')')
        
        if abiertos == cerrados:
            print(f"  [OK] Parentesis balanceados ({abiertos} pares)")
        else:
            print(f"  [ERROR] Parentesis NO balanceados: {abiertos} '(' vs {cerrados} ')'")
            return False
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error leyendo dominio: {e}")
        return False


def main():
    """Función principal."""
    resultado = validar_archivos()
    
    if resultado == 0:
        validar_pddl_sintaxis()
    
    print("\n" + "="*80)
    
    return resultado


if __name__ == "__main__":
    sys.exit(main())

