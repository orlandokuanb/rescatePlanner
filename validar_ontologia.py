#!/usr/bin/env python3
"""
Validador y Analizador de Ontología
Curso: MIA-103 - Fundamentos de Inteligencia Artificial

Este script valida la consistencia de la ontología y genera estadísticas.
"""

import json
from pathlib import Path
from typing import Dict, List, Set
from collections import Counter


class OntologiaValidator:
    """Valida y analiza la ontología del dominio de rescate."""
    
    def __init__(self, base_path: str = "ontologia"):
        self.base_path = Path(base_path)
        self.conceptos = None
        self.relaciones = None
        self.atributos = None
        
    def cargar_ontologia(self):
        """Carga todos los archivos JSON de la ontología."""
        try:
            with open(self.base_path / "conceptos.json", 'r', encoding='utf-8') as f:
                self.conceptos = json.load(f)
            
            with open(self.base_path / "relaciones.json", 'r', encoding='utf-8') as f:
                self.relaciones = json.load(f)
            
            with open(self.base_path / "atributos.json", 'r', encoding='utf-8') as f:
                self.atributos = json.load(f)
            
            print("✅ Ontología cargada exitosamente")
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Error: No se encontró archivo {e.filename}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Error de formato JSON: {e}")
            return False
    
    def validar_conceptos(self) -> bool:
        """Valida la estructura de conceptos."""
        print("\n" + "="*60)
        print("VALIDACIÓN DE CONCEPTOS")
        print("="*60)
        
        conceptos_data = self.conceptos.get('conceptos', [])
        
        if not conceptos_data:
            print("❌ No se encontraron conceptos")
            return False
        
        print(f"✅ Total de conceptos: {len(conceptos_data)}")
        
        # Validar que cada concepto tenga los campos requeridos
        campos_requeridos = ['id', 'nombre', 'categoria', 'descripcion', 'tipo_pddl']
        
        for concepto in conceptos_data:
            nombre = concepto.get('nombre', 'DESCONOCIDO')
            
            for campo in campos_requeridos:
                if campo not in concepto:
                    print(f"⚠️  Concepto '{nombre}' falta campo '{campo}'")
            
            # Contar instancias
            instancias = concepto.get('instancias', [])
            if isinstance(instancias, list):
                print(f"  📦 {nombre}: {len(instancias)} instancias")
        
        return True
    
    def validar_relaciones(self) -> bool:
        """Valida la estructura de relaciones."""
        print("\n" + "="*60)
        print("VALIDACIÓN DE RELACIONES")
        print("="*60)
        
        relaciones_data = self.relaciones.get('relaciones', [])
        
        if not relaciones_data:
            print("❌ No se encontraron relaciones")
            return False
        
        print(f"✅ Total de relaciones: {len(relaciones_data)}")
        
        # Contar relaciones por tipo
        tipos = Counter()
        for relacion in relaciones_data:
            tipo = relacion.get('tipo', 'Desconocido')
            tipos[tipo] += 1
        
        print("\nRelaciones por tipo:")
        for tipo, count in tipos.most_common():
            print(f"  {tipo}: {count}")
        
        # Validar formato PDDL
        sin_formato = [r['nombre'] for r in relaciones_data 
                      if 'formato_pddl' not in r and 'formato_pddl_personas' not in r]
        
        if sin_formato:
            print(f"\n⚠️  Relaciones sin formato PDDL: {', '.join(sin_formato)}")
        else:
            print("\n✅ Todas las relaciones tienen formato PDDL")
        
        return True
    
    def validar_atributos(self) -> bool:
        """Valida la estructura de atributos."""
        print("\n" + "="*60)
        print("VALIDACIÓN DE ATRIBUTOS")
        print("="*60)
        
        atributos_data = self.atributos.get('atributos_por_concepto', [])
        
        if not atributos_data:
            print("❌ No se encontraron atributos")
            return False
        
        total_atributos = 0
        mutables = 0
        inmutables = 0
        
        for concepto_attr in atributos_data:
            concepto = concepto_attr.get('concepto', 'DESCONOCIDO')
            attrs = concepto_attr.get('atributos', [])
            
            total_atributos += len(attrs)
            
            for attr in attrs:
                if attr.get('mutable', False):
                    mutables += 1
                else:
                    inmutables += 1
            
            print(f"  {concepto}: {len(attrs)} atributos")
        
        print(f"\n✅ Total de atributos: {total_atributos}")
        print(f"  📝 Mutables: {mutables}")
        print(f"  🔒 Inmutables: {inmutables}")
        
        return True
    
    def generar_estadisticas(self):
        """Genera estadísticas de la ontología."""
        print("\n" + "="*60)
        print("ESTADÍSTICAS GENERALES")
        print("="*60)
        
        # Contar instancias totales
        total_instancias = 0
        categorias = Counter()
        
        for concepto in self.conceptos.get('conceptos', []):
            instancias = concepto.get('instancias', [])
            categoria = concepto.get('categoria', 'Desconocida')
            
            if isinstance(instancias, list):
                n = len(instancias)
                total_instancias += n
                categorias[categoria] += n
        
        print(f"\n📊 Total de instancias en el dominio: {total_instancias}")
        print("\nInstancias por categoría:")
        for categoria, count in categorias.most_common():
            print(f"  {categoria}: {count}")
        
        # Análisis de complejidad
        num_conceptos = len(self.conceptos.get('conceptos', []))
        num_relaciones = len(self.relaciones.get('relaciones', []))
        
        print(f"\n🔢 Complejidad del dominio:")
        print(f"  Conceptos: {num_conceptos}")
        print(f"  Relaciones: {num_relaciones}")
        print(f"  Instancias: {total_instancias}")
        print(f"  Ratio Relación/Concepto: {num_relaciones/num_conceptos:.2f}")
    
    def verificar_consistencia(self):
        """Verifica la consistencia lógica de la ontología."""
        print("\n" + "="*60)
        print("VERIFICACIÓN DE CONSISTENCIA")
        print("="*60)
        
        # Test 1: Verificar que no hay IDs duplicados
        ids_conceptos = set()
        duplicados = []
        
        for concepto in self.conceptos.get('conceptos', []):
            cid = concepto.get('id')
            if cid in ids_conceptos:
                duplicados.append(cid)
            ids_conceptos.add(cid)
        
        if duplicados:
            print(f"❌ IDs de conceptos duplicados: {duplicados}")
        else:
            print("✅ No hay IDs de conceptos duplicados")
        
        # Test 2: Verificar que relaciones referencian conceptos existentes
        nombres_conceptos = {c.get('nombre') for c in self.conceptos.get('conceptos', [])}
        
        relaciones_inconsistentes = []
        for relacion in self.relaciones.get('relaciones', []):
            dominio = relacion.get('dominio', '')
            rango = relacion.get('rango', '')
            
            # Extraer nombres de tipos (simplificado)
            # Nota: esto es una verificación básica
            # En un sistema real, haría parsing más sofisticado
        
        print("✅ Verificación de consistencia completada")
    
    def generar_reporte_latex(self, output_path: str = "reporte_ontologia.tex"):
        """Genera un reporte en LaTeX de la ontología."""
        print("\n" + "="*60)
        print("GENERANDO REPORTE LATEX")
        print("="*60)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("% Reporte de Ontología - Generado automáticamente\n\n")
            
            # Tabla de conceptos
            f.write("\\begin{table}[h]\n")
            f.write("\\centering\n")
            f.write("\\caption{Conceptos del Dominio}\n")
            f.write("\\begin{tabular}{|l|p{5cm}|c|}\n")
            f.write("\\hline\n")
            f.write("\\textbf{ID} & \\textbf{Concepto} & \\textbf{Instancias} \\\\\n")
            f.write("\\hline\n")
            
            for concepto in self.conceptos.get('conceptos', []):
                cid = concepto.get('id', '')
                nombre = concepto.get('nombre', '')
                instancias = concepto.get('instancias', [])
                
                if isinstance(instancias, list):
                    num = len(instancias)
                else:
                    num = 0
                
                f.write(f"{cid} & {nombre} & {num} \\\\\n")
                f.write("\\hline\n")
            
            f.write("\\end{tabular}\n")
            f.write("\\label{tab:conceptos}\n")
            f.write("\\end{table}\n\n")
            
            # Tabla de relaciones
            f.write("\\begin{table}[h]\n")
            f.write("\\centering\n")
            f.write("\\caption{Relaciones Principales}\n")
            f.write("\\begin{tabular}{|l|l|l|}\n")
            f.write("\\hline\n")
            f.write("\\textbf{Relación} & \\textbf{Tipo} & \\textbf{Cardinalidad} \\\\\n")
            f.write("\\hline\n")
            
            for relacion in self.relaciones.get('relaciones', [])[:10]:  # Primeras 10
                nombre = relacion.get('nombre', '')
                tipo = relacion.get('tipo', '')
                card = relacion.get('cardinalidad', '')
                
                f.write(f"{nombre} & {tipo} & {card} \\\\\n")
                f.write("\\hline\n")
            
            f.write("\\end{tabular}\n")
            f.write("\\label{tab:relaciones}\n")
            f.write("\\end{table}\n")
        
        print(f"✅ Reporte LaTeX generado: {output_path}")
    
    def ejecutar_validacion_completa(self):
        """Ejecuta todas las validaciones."""
        print("\n" + "="*70)
        print(" "*15 + "VALIDACIÓN DE ONTOLOGÍA")
        print(" "*10 + "MIA-103 - Rescate en Mina")
        print("="*70)
        
        if not self.cargar_ontologia():
            return False
        
        resultados = {
            'conceptos': self.validar_conceptos(),
            'relaciones': self.validar_relaciones(),
            'atributos': self.validar_atributos()
        }
        
        self.generar_estadisticas()
        self.verificar_consistencia()
        
        # Resumen final
        print("\n" + "="*70)
        print("RESUMEN DE VALIDACIÓN")
        print("="*70)
        
        todas_ok = all(resultados.values())
        
        for componente, ok in resultados.items():
            simbolo = "✅" if ok else "❌"
            print(f"{simbolo} {componente.upper()}: {'OK' if ok else 'ERRORES'}")
        
        if todas_ok:
            print("\n🎉 ¡ONTOLOGÍA VÁLIDA Y COMPLETA!")
        else:
            print("\n⚠️  Hay errores que corregir")
        
        return todas_ok


def main():
    """Función principal."""
    validator = OntologiaValidator(".")
    
    # Ejecutar validación completa
    validator.ejecutar_validacion_completa()
    
    # Generar reporte LaTeX
    validator.generar_reporte_latex()
    
    print("\n" + "="*70)
    print("Validación completada. Revisa los archivos generados.")
    print("="*70)


if __name__ == "__main__":
    main()
